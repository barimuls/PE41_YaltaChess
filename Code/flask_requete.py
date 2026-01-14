from flask import Flask, request, jsonify, render_template
from Plateau import *
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)
compteur = 0
L_requete = [None,None]
plateau = creer_plateau()
plateau.remplir_arete()
plateau.remplir_pieces_initiales()
plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)
n_ligne = False
type_ia = None

@app.context_processor
def inject_plateau_piece():
    return dict(plateau_pieces=plateau_pieces)


@app.context_processor
def inject_plateau_couleur():
    return dict(plateau_couleurs=plateau_couleurs)


@app.route('/')
def index():
    return render_template('index.html')


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


@app.route('/receive', methods=['POST'])
def receive():
    global compteur, L_requete, plateau_pieces, plateau_couleurs, plateau, n_ligne, type_ia
    data = request.get_json()
    value = data.get('value')
    print(value)
    if value[:2] == 'ia':
        n_ligne = False
        type_ia = value
        compteur = 0
        L_requete = [None,None]
        plateau = creer_plateau()
        plateau.remplir_arete()
        plateau.remplir_pieces_initiales()
        plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)
        if value == 'ia_aleatoire':
            return jsonify({"reponse": "Mode IA aléatoire activé"})
        if value == 'ia_heuristique':
            return jsonify({"reponse": "Mode IA heuristique activé"})
        
    if value == '3joueurs':
        compteur = 0
        L_requete = [None,None]
        plateau = creer_plateau()
        plateau.remplir_arete()
        plateau.remplir_pieces_initiales()
        plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)
        n_ligne = True
        return jsonify({"reponse": "Mode en ligne activé"})
    if value == 'reset':
        compteur = 0
        L_requete = [None,None]
        plateau = creer_plateau()
        plateau.remplir_arete()
        plateau.remplir_pieces_initiales()
        plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)
        return jsonify({"reponse": "Partie réinitialisée"})
    if value in ['promotion_tour', 'promotion_fou', 'promotion_cavalier', 'promotion_dame']:
        piece_map = {
            'promotion_tour': 'tour',
            'promotion_fou': 'fou',
            'promotion_cavalier': 'cavalier',
            'promotion_dame': 'dame'
        }
        piece_type = piece_map[value]
        if not n_ligne:
            couleur = 0
        if n_ligne:
            couleur = (compteur//2-1)%3
        promotion(plateau, L_requete[1], couleur, piece_type)
        plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)
        return jsonify({"reponse": f"Pion promu en {piece_type}"})
    L_requete[compteur%2] = value.lower()
    print(f"Valeur reçue : {value}")
    print(compteur)
    depart = L_requete[0]
    arrivee = L_requete[1]
    print(L_requete)
    if compteur % 2 == 1 and L_requete[0] is not None and L_requete[1] is not None:
        print(">>> depart:", depart, "arrivee:", arrivee, "type:", type(arrivee))
        if n_ligne:
            if tour_de_jeu_web(plateau,(compteur//2)%3, depart, arrivee)==False:
                compteur += -1
                plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)
                return jsonify({"reponse": "Mouvement invalide"})
        if not n_ligne:
            if type_ia == 'ia_aleatoire':
                if tour_de_jeu_avec_IA_web(plateau, depart, arrivee)==False:
                    compteur += -1
                    plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)
                    return jsonify({"reponse": "Mouvement invalide"})
            if type_ia == 'ia_heuristique':
                if tour_de_jeu_IA_minimax_web_ou_on_dejoue(plateau, depart, arrivee)==False:
                    compteur += -1
                    plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)
                    return jsonify({"reponse": "Mouvement invalide"})
    compteur += 1
    plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)
    if verifier_victoire(plateau, (compteur//2)%3)==True:
        if n_ligne:
            return jsonify({"reponse": f"Le joueur {(compteur//2)%3-1} a gagné!"})
        return jsonify({"reponse": f"Le joueur {(compteur//2)%3} a gagné!"})
    if compteur % 2 == 1 and L_requete[0] is not None and L_requete[1] is not None and not n_ligne:
        return jsonify({"reponse": value + " faite votre 2ème action et patientez le tour de l'IA"})
    return jsonify({"reponse": value})

@socketio.on('connect')
def handle_connect():
    emit('update', {'message': 'Connexion établie'})

def envoyer_mise_a_jour():
    global plateau_pieces, plateau_couleurs
    while True:
        socketio.emit('update', {'plateau_pieces': plateau_pieces, 'plateau_couleurs': plateau_couleurs})
        socketio.sleep(0.5)

if __name__ == '__main__':
    socketio.start_background_task(envoyer_mise_a_jour)
    socketio.run(app, debug=True,allow_unsafe_werkzeug=True)