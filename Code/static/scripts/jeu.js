
let cl = "blanc";
let cmpt = 0;
let mode = "3joueurs";

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
    tour.src = "/static/images/tour_" + cl + ".svg";
    tour.alt = "tour_" + cl;
    tour.width = 70;
    tour.onclick = () => closeModal('promotion_tour');
    tour.style = "margin:20px";
    document.getElementById('modal').appendChild(tour);
    fou = document.createElement("img");
    fou.src = "/static/images/fou_" + cl + ".svg";
    fou.alt = "fou_" + cl;
    fou.width = 70;
    fou.onclick = () => closeModal('promotion_fou');
    fou.style = "margin:20px";
    document.getElementById('modal').appendChild(fou);
    cavalier = document.createElement("img");
    cavalier.src = "/static/images/cavalier_" + cl + ".svg";
    cavalier.alt = "cavalier_" + cl;
    cavalier.width = 70;
    cavalier.onclick = () => closeModal('promotion_cavalier');
    cavalier.style = "margin:20px";
    document.getElementById('modal').appendChild(cavalier);
    dame = document.createElement("img");
    dame.src = "/static/images/dame_" + cl + ".svg";
    dame.alt = "dame_" + cl;
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
socket.on('update', data => {
    if (!gameId || data.game_id !== gameId) return;
    console.log("Mise à jour reçue :", data);
    console.log("Comparaison :", data.game_id, gameId, data.game_id === gameId);
    const pieces = data.plateau_pieces;
    const couleurs = data.plateau_couleurs;
    mode = data.mode;
    genererToutesLesPieces(data);
    for (const caseId in pieces) {
        const piece = pieces[caseId];
        const couleur = couleurs[caseId];
        const num = +caseId.slice(1, caseId.length);
        cl = couleur;
        if (piece === "pion") {
            if ([1, 8, 12].includes(num)) {
                // Demander une promotion de pion
                openModal();

            }
        }
    }
    console.log("Compteur de tours :", cmpt);
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
    if (mode === 'multijoueur') {window.joueurActuel = data.joueur;}

    fetch("/game/search_player/" + gameId, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
    })
    .then(res => res.json())
    .then(data2 => {
        const joueurEl = document.getElementById("joueur");
        if (joueurEl) {joueurEl.textContent = data2.player_index;}
    })
    .catch(err => console.error("Erreur lors de la récupération du joueur actuel :", err));
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
        Document.getElementById(caseId).id = (sens === "gauche") ? rotateLeft[caseId] : rotateRight[caseId];
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
