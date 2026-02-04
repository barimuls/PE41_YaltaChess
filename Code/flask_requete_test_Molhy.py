from flask import Flask, request, jsonify, render_template
from Plateau import *
from FonctionJeux import *
from flask_socketio import SocketIO, emit

# Création de l'application Flask
app = Flask(__name__)

# Initialisation de SocketIO pour communication temps réel
socketio = SocketIO(app)

# Compteur servant à savoir si on est sur sélection départ ou arrivée
compteur = 0

# Liste qui stocke la case de départ et d’arrivée
L_requete = [None, None]

# Création du plateau de jeu
plateau = creer_plateau()

# Remplit les bordures du plateau
plateau.remplir_arete()

# Place les pièces initiales
plateau.remplir_pieces_initiales()

# Convertit le plateau en données exploitables par le site
plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)

# Variable indiquant si le jeu est en ligne ou local
est_en_ligne = False


# Permet d'envoyer automatiquement les pièces du plateau aux templates HTML
@app.context_processor
def inject_plateau_piece():
    return dict(plateau_pieces=plateau_pieces)


# Permet d'envoyer les couleurs du plateau aux templates HTML
@app.context_processor
def inject_plateau_couleur():
    return dict(plateau_couleurs=plateau_couleurs)


# Route page d'accueil
@app.route('/')
def index():
    return render_template('index.html')


# Routes secondaires affichant différentes pages
@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/test2')
def test2():
    return render_template('test2.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/jeu')
def jeu():
    return render_template('jeu.html')


# Route principale qui reçoit les actions du joueur
@app.route('/receive', methods=['POST'])
def receive():

    # Déclaration des variables globales modifiées dans la fonction
    global compteur, L_requete, plateau_pieces, plateau_couleurs, plateau, est_en_ligne

    # Récupère les données envoyées depuis le site
    data = request.get_json()
    value = data.get('value')
    print(value)

    # ----- MODE LOCAL -----
    if value == 'local':
        est_en_ligne = False
        compteur = 0
        L_requete = [None, None]

        # Réinitialise le plateau
        plateau = creer_plateau()
        plateau.remplir_arete()
        plateau.remplir_pieces_initiales()

        plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)

        return jsonify({"reponse": "Mode local activé"})

    # ----- MODE EN LIGNE -----
    if value == 'ligne':
        compteur = 0
        L_requete = [None, None]

        plateau = creer_plateau()
        plateau.remplir_arete()
        plateau.remplir_pieces_initiales()

        plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)

        est_en_ligne = True

        return jsonify({"reponse": "Mode en ligne activé"})

    # ----- RESET PARTIE -----
    if value == 'reset':
        compteur = 0
        L_requete = [None, None]

        plateau = creer_plateau()
        plateau.remplir_arete()
        plateau.remplir_pieces_initiales()

        plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)

        return jsonify({"reponse": "Partie réinitialisée"})

    # ----- GESTION PROMOTION PION -----
    if value in ['promotion_tour', 'promotion_fou', 'promotion_cavalier', 'promotion_dame']:

        # Associe la commande reçue au type de pièce
        piece_map = {
            'promotion_tour': 'tour',
            'promotion_fou': 'fou',
            'promotion_cavalier': 'cavalier',
            'promotion_dame': 'dame'
        }

        piece_type = piece_map[value]

        # Détermine la couleur du joueur
        if not est_en_ligne:
            couleur = 0
        else:
            couleur = (compteur // 2 - 1) % 3

        # Applique la promotion
        promotion(plateau, L_requete[1], couleur, piece_type)

        plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)

        return jsonify({"reponse": f"Pion promu en {piece_type}"})

    # Stocke la case sélectionnée (départ ou arrivée)
    L_requete[compteur % 2] = value.lower()

    print(f"Valeur reçue : {value}")
    print(compteur)

    depart = L_requete[0]
    arrivee = L_requete[1]

    print(L_requete)

    # Si on a sélectionné départ ET arrivée
    if compteur % 2 == 1 and L_requete[0] is not None and L_requete[1] is not None:

        print(">>> depart:", depart, "arrivee:", arrivee)

        # ----- MODE EN LIGNE -----
        if est_en_ligne:
            if tour_de_jeu_web(plateau, (compteur // 2) % 3, depart, arrivee) == False:
                compteur += -1
                plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)
                return jsonify({"reponse": "Mouvement invalide"})

        # ----- MODE IA -----
        else:
            if tour_de_jeu_IA_minimax_web_ou_on_dejoue(plateau, depart, arrivee) == False:
                compteur += -1
                plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)
                return jsonify({"reponse": "Mouvement invalide"})

    # Passe au clic suivant
    compteur += 1

    # Met à jour affichage plateau
    plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)

    # Vérifie victoire
    if verifier_victoire(plateau, (compteur // 2) % 3) == True:

        if est_en_ligne:
            return jsonify({"reponse": f"Le joueur {(compteur // 2) % 3 - 1} a gagné!"})

        return jsonify({"reponse": f"Le joueur {(compteur // 2) % 3} a gagné!"})

    return jsonify({"reponse": value})


# Quand un client se connecte au serveur SocketIO
@socketio.on('connect')
def handle_connect():
    emit('update', {'message': 'Connexion établie'})


# Envoie régulièrement le plateau aux clients
def envoyer_mise_a_jour():
    global plateau_pieces, plateau_couleurs

    while True:
        socketio.emit('update', {
            'plateau_pieces': plateau_pieces,
            'plateau_couleurs': plateau_couleurs
        })

        socketio.sleep(0.5)


# Lancement du serveur
if __name__ == '__main__':

    # Lance la tâche d'envoi des mises à jour
    socketio.start_background_task(envoyer_mise_a_jour)

    # Lance le serveur Flask + SocketIO
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
