
let couleur = "blanc";
let cmpt = 0;
let mode = "3joueurs";

let monIndex = 0;

// Au chargement de la page, on récupère qui on est
fetch("/game/search_player/" + gameId, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
})
.then(res => res.json())
.then(data2 => {
    console.log("Réponse seach_player:", data2);
    const couleurToIndex = { blanc: 0, rouge: 1, noir: 2 };
    monIndex = couleurToIndex[data2.player_index] ?? 0;
    console.log("Je suis le joueur :", data2.player_index, "→ index", monIndex);
})
.catch(() => { monIndex = 0; });

const rotateLeft = {A1 : "L8", A2 : "L7", A3 : "L6", A4 : "L5", A5 : "L9", A6 : "L10", A7 : "L11", A8 : "L12",
                    B1 : "K8", B2 : "K7", B3 : "K6", B4 : "K5", B5 : "K9", B6 : "K10", B7 : "K11", B8 : "K12",
                    C1 : "J8", C2 : "J7", C3 : "J6", C4 : "J5", C5 : "J9", C6 : "J10", C7 : "J11", C8 : "J12",
                    D1 : "I8", D2 : "I7", D3 : "I6", D4 : "I5", D5 : "I9", D6 : "I10", D7 : "I11", D8 : "I12",
                    L8 : "H12", L7 : "H11", L6 : "H10", L5 : "H9", L9 : "H4", L10 : "H3", L11 : "H2", L12 : "H1",
                    K8 : "G12", K7 : "G11", K6 : "G10", K5 : "G9", K9 : "G4", K10 : "G3", K11 : "G2", K12 : "G1",
                    J8 : "F12", J7 : "F11", J6 : "F10", J5 : "F9", J9 : "F4", J10 : "F3", J11 : "F2", J12 : "F1",
                    I8 : "E12", I7 : "E11", I6 : "E10", I5 : "E9", I9 : "E4", I10 : "E3", I11 : "E2", I12 : "E1",
                    H12 : "A1", H11 : "A2", H10 : "A3", H9 : "A4", H4 : "A5", H3 : "A6", H2 : "A7", H1 : "A8",
                    G12 : "B1", G11 : "B2", G10 : "B3", G9 : "B4", G4 : "B5", G3 : "B6", G2 : "B7", G1 : "B8",
                    F12 : "C1", F11 : "C2", F10 : "C3", F9 : "C4", F4 : "C5", F3 : "C6", F2 : "C7", F1 : "C8",
                    E12 : "D1", E11 : "D2", E10 : "D3", E9 : "D4", E4 : "D5", E3 : "D6", E2 : "D7", E1 : "D8"};

const rotateRight = {};
for (const from in rotateLeft) {
    const to = rotateLeft[from];
    rotateRight[to] = from;
}

function openModal() {
    document.getElementById('modal').querySelectorAll("img").forEach(img => img.remove());
    tour = document.createElement("img");
    tour.src = "/static/images/tour_" + couleur + ".svg";
    tour.alt = "tour_" + couleur;
    tour.width = 70;
    tour.onclick = () => closeModal('promotion_tour');
    tour.style = "margin:20px";
    document.getElementById('modal').appendChild(tour);
    fou = document.createElement("img");
    fou.src = "/static/images/fou_" + couleur + ".svg";
    fou.alt = "fou_" + couleur;
    fou.width = 70;
    fou.onclick = () => closeModal('promotion_fou');
    fou.style = "margin:20px";
    document.getElementById('modal').appendChild(fou);
    cavalier = document.createElement("img");
    cavalier.src = "/static/images/cavalier_" + couleur + ".svg";
    cavalier.alt = "cavalier_" + couleur;
    cavalier.width = 70;
    cavalier.onclick = () => closeModal('promotion_cavalier');
    cavalier.style = "margin:20px";
    document.getElementById('modal').appendChild(cavalier);
    dame = document.createElement("img");
    dame.src = "/static/images/dame_" + couleur + ".svg";
    dame.alt = "dame_" + couleur;
    dame.width = 70;
    dame.onclick = () => closeModal('promotion_dame');
    dame.style = "margin:20px";
    document.getElementById('modal').appendChild(dame);
    document.getElementById('overlay').style.display = 'flex';

}

function highlightCase(id, color = "#00aaff88") {
    const poly = document.getElementById(id);
    if (!poly) return;

    // Créer un nouveau polygon
    const overlay = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
    overlay.setAttribute("points", poly.getAttribute("points"));
    overlay.setAttribute("fill", color);
    overlay.setAttribute("id", id + "_overlay");
    overlay.style.pointerEvents = "none"; // pour ne pas bloquer les clics

    // Ajouter juste après la case originale
    poly.parentNode.insertBefore(overlay, poly.nextSibling);
}

function clearAllHighlights() {
    document.querySelectorAll("polygon[id$='_overlay']").forEach(el => el.remove());
}


function closeModal(piece) {
    sendValue(piece);
    document.getElementById('overlay').style.display = 'none';
}
// --- 1️⃣ Fonction pour envoyer les coups au backend Flask ---
function sendValue(maValeur) {
    clearAllHighlights();

    if (!gameId) return;
    if (mode === "multijoueur" && window.joueurActuel !== localStorage.getItem("user_id")) {return;} // ce n'est pas ton tour
        
    // Si c'est une case du plateau, on dé-rote vers les coordonnées réelles du serveur
    if (maValeur.length <= 3 && !maValeur.startsWith("promotion_") && maValeur !== "reset") {
        const nbRot = getNbRotations(monIndex);
        // Rotation inverse : on applique rotateRight nbRot fois
        let vraiCase = maValeur;
        for (let i = 0; i < nbRot; i++) {
            vraiCase = rotateLeft[vraiCase] ?? vraiCase;
        }
        console.log("Clic visuel:", maValeur, "/ monIndex:", monIndex, "/nbRot:", nbRot, "Case envoyée", vraiCase);
        maValeur = vraiCase;
    }

    let endpoint = "";

    // PROMOTION
    if (maValeur.startsWith("promotion_")) {
        const piece = maValeur.replace("promotion_", "");
        endpoint = `/receive/promotion/${gameId}`;
        maValeur = piece;
    }

    // RESET
    else if (maValeur === "reset") {
        endpoint = `/receive/reset/${gameId}`;
        cmpt = 0;
    }

    // CLIC 1 = départ
    else if (maValeur.length <= 3 && cmpt % 2 === 0) {
        endpoint = `/receive/depart/${gameId}`;
        cmpt++;  // on avance le compteur
    }

    // CLIC 2 = arrivée
    else if (maValeur.length <= 3 && cmpt % 2 === 1) {
        endpoint = `/receive/arrivee/${gameId}`;
        cmpt++;  // on avance le compteur
    }

    if (!endpoint) return;
    let payload = { value: maValeur };

    if (mode === "multijoueur") {
        payload.player = localStorage.getItem("user_id");
    }

    fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        const resultEl = document.getElementById("resultat");
        if (resultEl) resultEl.textContent = data.reponse;

        // --- Correction : si mouvement impossible → reset du compteur ---
        if (data.reponse === "Mouvement invalide") {
            cmpt = 0;
            return;
        }

        if (data.reponse.slice(0,8) === "Victoire") {
            console.log("Victoire détectée, désactivation du plateau");
            const pieces = data.plateau_pieces;
            console.log("Pièces sur le plateau :", pieces);
            for (const caseId in pieces) {
                console.log(caseId);
                document.getElementById(caseId).style.pointerEvents = "none";
            }
            const elems = document.getElementsByClassName("pointer-events-none");
            for (let el of elems) {
                el.style.pointerEvents = "none";
            }
        }

        if (data.reponse === "Partie réinitialisée") {
            const pieces = data.plateau_pieces;
            for (const caseId in pieces) {
                document.getElementById(caseId).style.pointerEvents = "auto";
            }
            const elems = document.getElementsByClassName("pointer-events-none");
            for (let el of elems) {
                el.style.pointerEvents = "auto";
            }
        }

        // Coups possibles (clic 1)
        if (data.coup_possible) {
            for (const caseId of data.coup_possible) {
                highlightCase(caseId);
            }
        }
    })
    .catch(error => console.error("Erreur lors de l’envoi :", error));
}




// --- 2️ Connexion au serveur Socket.IO ---
const socket = io();

socket.on('connect', () => {
    console.log("Connecté à SocketIO");
    socket.emit("join_game", { game_id: gameId });
});


// ---  Réception des mises à jour automatiques du plateau ---
// Variable globale pour stocker l'index du joueur local
monIndex = 0; // 0=blanc par défaut

socket.on('update', data => {
    if (!gameId || data.game_id !== gameId) return;

    mode = data.mode;

    // Mise à jour des indicateurs de tour
    if (data.joueur === 0) {
        document.getElementById("t_blanc").setAttribute("fill", "#769656");
        document.getElementById("t_rouge").setAttribute("fill", "#FFFFFF");
        document.getElementById("t_noir").setAttribute("fill", "#FFFFFF");
    } else if (data.joueur === 1) {
        document.getElementById("t_blanc").setAttribute("fill", "#FFFFFF");
        document.getElementById("t_rouge").setAttribute("fill", "#769656");
        document.getElementById("t_noir").setAttribute("fill", "#FFFFFF");
    } else {
        document.getElementById("t_blanc").setAttribute("fill", "#FFFFFF");
        document.getElementById("t_rouge").setAttribute("fill", "#FFFFFF");
        document.getElementById("t_noir").setAttribute("fill", "#769656");
    }

    if (mode === 'multijoueur') { window.joueurActuel = data.joueur; }

    // On récupère d'abord l'index du joueur, PUIS on affiche le plateau
    fetch("/game/search_player/" + gameId, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
    })
    .then(res => res.json())
    .then(data2 => {
        // Mettre à jour l'affichage du joueur
        const joueurEl = document.getElementById("joueur");
        if (joueurEl) { joueurEl.textContent = data2.player_index; }

        const nbRot = getNbRotations(monIndex);

        // Remapper les données du plateau selon la rotation
        const { pieces: piecesRot, couleurs: couleursRot } = remapPlateau(
            data.plateau_pieces,
            data.plateau_couleurs,
            nbRot
        );
        const dataRotated = { ...data, plateau_pieces: piecesRot, plateau_couleurs: couleursRot };

        // Afficher les pièces avec la rotation appliquée
        genererToutesLesPieces(dataRotated);

        // Vérification promotion sur les données remappées
        for (const caseId in piecesRot) {
            const piece = piecesRot[caseId];
            const num = +caseId.slice(1);
            if (piece === "pion" && [1, 8, 12].includes(num)) {
                couleur = couleursRot[caseId];
                openModal();
            }
        }
    })
    .catch(err => {
        // En mode non-multijoueur, search_player retourne null → on affiche sans rotation
        console.warn("Pas de joueur trouvé, affichage sans rotation");
        genererToutesLesPieces(data);

        // Vérification promotion sans rotation
        for (const caseId in data.plateau_pieces) {
            const piece = data.plateau_pieces[caseId];
            const num = +caseId.slice(1);
            if (piece === "pion" && [1, 8, 12].includes(num)) {
                couleur = data.plateau_couleurs[caseId];
                openModal();
            }
        }
    });
});
function polygonCentroid(points) {
    let cx = 0, cy = 0;
    let area = 0;

    for (let i = 0; i < points.length; i++) {
        const j = (i + 1) % points.length;
        const cross = points[i].x * points[j].y - points[j].x * points[i].y;
        area += cross;
        cx += (points[i].x + points[j].x) * cross;
        cy += (points[i].y + points[j].y) * cross;
    }

    area *= 0.5;
    cx /= (6 * area);
    cy /= (6 * area);

    return { x: cx, y: cy };
}

function centerHTMLImageOnPolygon(polygonId, imgId) {
    const polygon = document.getElementById(polygonId);
    const img = document.getElementById(imgId);
    const main = document.querySelector("main");

    // Lire les points du polygon
    const points = polygon
        .getAttribute("points")
        .trim()
        .split(/\s+/)
        .map(p => {
            const [x, y] = p.split(",").map(Number);
            return { x, y };
        });

    // Calcul du centroïde géométrique
    const { x: cx, y: cy } = polygonCentroid(points);

    // Conversion SVG → écran
    const svg = polygon.ownerSVGElement;
    const pt = svg.createSVGPoint();
    pt.x = cx;
    pt.y = cy;
    const screenPos = pt.matrixTransform(svg.getScreenCTM());
    // Décalage par rapport à <main>
    const mainRect = main.getBoundingClientRect();
    const trueX = screenPos.x - mainRect.left;
    const trueY = screenPos.y - mainRect.top;

    // Positionner l'image
    img.style.position = "absolute";
    img.style.left = `${trueX}px`;
    img.style.top = `${trueY}px`;
    img.style.transform = "translate(-50%, -50%)";
}

function rotationPlateau(data, sens) {
    const pieces = data.plateau_pieces;
    const cases = Object.keys(pieces);
    if (sens != "none") {
    for (const caseId of cases) {
        document.getElementById(caseId).id = (sens === "gauche") ? rotateLeft[caseId] : rotateRight[caseId];
    }
    }
}


function genererToutesLesPieces(data) {
    const pieces = data.plateau_pieces;
    console.log("Pièces sur le plateau :", pieces);
    const couleurs = data.plateau_couleurs;
    const main = document.querySelector("main");

    // Supprimer toutes les anciennes images
    document.querySelectorAll("main img").forEach(img => { if (!img.closest(".modal")) { img.remove(); } });


    for (const caseId in pieces) {
        const piece = pieces[caseId];
        const couleur = couleurs[caseId];

        if (!piece || !couleur) continue;

        const imgId = piece + "_" + caseId;

        const img = document.createElement("img");
        img.id = imgId;
        img.className = piece + "_" + couleur;
        img.alt = piece;
        img.width = 27;
        img.src = `/static/images/${piece}_${couleur}.svg`;

        img.style.position = "absolute";
        img.style.zIndex = "2";
        img.style.pointerEvents = "none";
        img.style.transform = "translate(-140%, -130%)";
        img.style.userSelect = "none";

        main.appendChild(img);
        centerHTMLImageOnPolygon(caseId, imgId);

    }
}

// c'est claud, si vous avez des questions sur le code, n'hésitez pas à pas me demander 

// =============================================
// ROTATION DES DONNÉES (pas du SVG)
// =============================================

// Applique N fois rotateLeft sur une caseId
function rotateCase(caseId, n) {
    let result = caseId;
    for (let i = 0; i < n; i++) {
        result = rotateLeft[result] ?? result;
    }
    return result;
}

// Retourne un nouveau plateau_pieces/couleurs avec les cases remappées
function remapPlateau(pieces, couleurs, nbRotations) {
    if (nbRotations === 0) return { pieces, couleurs };
    const newPieces = {};
    const newCouleurs = {};
    for (const caseId in pieces) {
        const newId = rotateCase(caseId, nbRotations);
        newPieces[newId] = pieces[caseId];
        newCouleurs[newId] = couleurs[caseId];
    }
    return { pieces: newPieces, couleurs: newCouleurs };
}

// Détermine combien de rotations appliquer selon le joueur local
function getNbRotations(monIndex) {
    // monIndex : 0=blanc, 1=rouge, 2=noir
    // On veut que chaque joueur voie ses pièces en bas
    // blanc=0 rot, rouge=1 rot, noir=2 rot
    return (3-monIndex)%3; // à ajuster selon le sens de votre plateau
} // a mon avis ca sert à rien mais je laisse au cas où

