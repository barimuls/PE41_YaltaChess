
let cl = "blanc";
let cmpt = 0;

function goToTutoriel(mode) {

    // 1. Créer une nouvelle partie côté serveur
    fetch("/new_game", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mode: mode })
    })
    .then(res => res.json())
    .then(data => {

        const gameId = data.game_id;
        console.log("Nouvelle partie créée :", gameId);

        // 2. Redirection vers la page du tutoriel
        window.location.href = `/tutoriel/${gameId}`;
    })
    .catch(err => console.error("Erreur lors de la création de la partie :", err));
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

function closeModal(piece) {
    sendValue(piece);
    document.getElementById('overlay').style.display = 'none';
}
// --- 1️⃣ Fonction pour envoyer les coups au backend Flask ---
function sendValue(maValeur) {
    if (!gameId) {
        console.error("ID de jeu non défini !");
        return;
    }
    fetch(`/receive/${gameId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ value: maValeur })
    })
        .then(res => res.json())
        .then(data => {
            // Affiche la réponse du serveur (par exemple "Mouvement invalide")
            const resultEl = document.getElementById("resultat");
            if (resultEl) resultEl.textContent = data.reponse;
            console.log("Valeur envoyée :", maValeur);
            if (data.reponse.length >= 2 & data.reponse.length <= 3) {
                cmpt += 1;
            }
            if (data.reponse === "Partie réinitialisée") {
                cmpt = 0;
            }
            if (data.reponse === "Mouvement invalide") {
                cmpt += -1;
            }

        })
        .catch(error => console.error('Erreur lors de l’envoi :', error));
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


function genererToutesLesPieces(data) {
    const pieces = data.plateau_pieces;
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

        main.appendChild(img);
        centerHTMLImageOnPolygon(caseId, imgId);

    }
}
