function openModalConnexion() {
    if (document.getElementById('overlay_connexion').style.display === 'flex') {
        document.getElementById('overlay_connexion').style.display = 'none';
    }
    else {
        document.getElementById('overlay_connexion').style.display = 'flex';
    }
}

function logout() {
    fetch("/auth/logout")
        .then(res => res.json())
        .catch(err => console.error("Erreur lors de la déconnexion :", err));
}