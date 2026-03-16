
function openModal(x) {
    document.getElementById('overlay' + x).style.display = 'flex';
}

function openModalConnexion() {
    if (document.getElementById('overlay_connexion').style.display === 'flex') {
        document.getElementById('overlay_connexion').style.display = 'none';
    }
    else {
        document.getElementById('overlay_connexion').style.display = 'flex';
    }
}

function closeModal(x) {
    document.getElementById('overlay' + x).style.display = 'none';
}

function returnModal(x, y) {
    closeModal(x);
    openModal(y);
}

function ModalErreur(x) {
    if (x != undefined) {
        closeModal(x);
    }
    openModal(3);
}

function goToJeu(mode) {

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

        // 2. Redirection vers la page du jeu
        window.location.href = `/jeu/${gameId}`;
    })
    .catch(err => console.error("Erreur lors de la création de la partie :", err));
}

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

