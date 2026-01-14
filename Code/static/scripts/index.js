function sendValue(maValeur) {
    fetch('/receive', {
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
        })
        .catch(error => console.error("Erreur lors de l’envoi :", error));
}

function openModal(x) {
    document.getElementById('overlay' + x).style.display = 'flex';
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

function goToJeu(maValeur) {
    sendValue(maValeur);
    window.location.href = urljeu;
}