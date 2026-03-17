function openModalConnexion() {
    if (document.getElementById('overlay_connexion').style.display === 'flex') {
        document.getElementById('overlay_connexion').style.display = 'none';
    }
    else {
        document.getElementById('overlay_connexion').style.display = 'flex';
    }
}

document.addEventListener("DOMContentLoaded", function () {
    user();
});

function user() {
    // 1. Créer une nouvelle partie côté serveur
    fetch("/auth/me", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
    })
    .then(res => res.json())
    .then(data => {

        const loggedIn = data.loggedIn;
        console.log("Utilisateur connecté :", loggedIn);
        if (loggedIn) {
            const username = data.username;
            console.log("Utilisateur connecté :", username);
            document.getElementById("username_display").textContent = username;
            document.getElementById("username_display").removeAttribute("href");
        }
        else {
            console.log("Aucun utilisateur connecté");
            document.getElementById("username_display").textContent = "Veuillez-vous connecter";
            document.getElementById("username_display").href = "/login";
        }
    })
    .catch(err => console.error("Erreur lors de la lecture des informations utilisateur :", err));
}

function logout() {
    fetch("/auth/logout")
        .then(res => res.json())
        .catch(err => console.error("Erreur lors de la déconnexion :", err));
}

