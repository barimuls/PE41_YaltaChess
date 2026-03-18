const socket = io();

function openModal(x) {
    document.getElementById('overlay' + x).style.display = 'flex';
}

function openLobby() {
    fetch("/auth/me", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
    })
    .then(res => res.json())
    .then(data => {

        const loggedIn = data.loggedIn;
        console.log("Utilisateur connecté :", loggedIn);
        if (loggedIn) {
            socket.emit("register", { user_id: localStorage.getItem("user_id") });
            openModal('_lobby');
            fetch("/lobby/join", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: localStorage.getItem("user_id") })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === "waiting") {
                    document.getElementById("filedattente").textContent = data.position ? `Position dans la file d'attente : ${data.position}` : "Vous êtes en tête de la file d'attente, en attente d'un adversaire...";
                }
                else if (data.status === "matched" && data.players.includes(localStorage.getItem("user_id"))) {
                    window.location.href = `/jeu/${data.game_id}`;
                }
            }
            
            )
            .catch(err => console.error("Erreur lors de la connexion au lobby :", err));
        }
        else {
            window.location.href = "/login";
        }
    })
    .catch(err => console.error("Erreur lors de la lecture des informations utilisateur :", err));
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

function logout() {
    fetch("/auth/logout")
        .then(res => res.json())
        .catch(err => console.error("Erreur lors de la déconnexion :", err));
}

socket.on("matched", data => {
    window.location.href = `/jeu/${data.game_id}`;
});
