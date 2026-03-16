function openModalConnexion() {
    if (document.getElementById('overlay_connexion').style.display === 'flex') {
        document.getElementById('overlay_connexion').style.display = 'none';
    }
    else {
        document.getElementById('overlay_connexion').style.display = 'flex';
    }
}