import uuid
from flask import Flask, request, jsonify, render_template
from Plateau import *
from flask_socketio import SocketIO, emit
from FonctionJeux import *
from FonctionJeuxIA import *;

app = Flask(__name__)
socketio = SocketIO(app)

def nouvelle_partie(mode):
    plateau = creer_plateau()
    plateau.remplir_arete()
    plateau.remplir_pieces_initiales()
    plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)

    return {
        "compteur_clic": 0, # Compteur servant à savoir si on est sur sélection départ ou arrivée
        "compteur_tour": 0, # Compteur servant à savoir quel joueur doit jouer
        "plateau": plateau,
        "plateau_pieces": plateau_pieces,
        "plateau_couleurs": plateau_couleurs,
        "mode": mode, # 3joueurs ou ia_heuristique ou ia_aleatoire 
        "depart": None # Case de départ sélectionnée
        }

games = {} # contiendra l'ensemble de la partie { l'identifiant de la partie: {"compteur":#, ...} }


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

# renvoie sur la partie d'identifiant: game_id
@app.route('/jeu/<game_id>')
def jeu(game_id):
    return render_template("jeu.html", game_id=game_id)

# création d'une nouvelle partie et choix du mode
@app.route('/new_game', methods=['POST'])
def new_game():
    data = request.get_json()
    mode = data.get("mode", "reset")
    game_id = uuid.uuid4().hex[:8] # génere 64 caracteres aléatoires et selectionne les 8 premiers 
    games[game_id] = nouvelle_partie(mode)
    return jsonify({"game_id": game_id})

@app.route('/receive/<game_id>', methods=['POST'])
def receive(game_id):
    if game_id not in games:
        return jsonify({"error": "Partie inconnue"}), 404
    game = games[game_id]
    data = request.get_json()
    value = data.get('value')
    
    # RESET la partie dans le meme mode avec le meme identifiant
    if value == 'reset':
        games[game_id] = nouvelle_partie(game["mode"])
        envoyer_mise_a_jour(game_id)
        return jsonify({"reponse": "Partie réinitialisée"})

    # PROMOTION
    if value in ['promotion_tour', 'promotion_fou', 'promotion_cavalier', 'promotion_dame']:
        piece_map = {
            'promotion_tour': 'tour',
            'promotion_fou': 'fou',
            'promotion_cavalier': 'cavalier',
            'promotion_dame': 'dame'
        }
        piece_type = piece_map[value]
        if not game["mode"] == "3joueurs":
            couleur = 0 
        else:
            couleur = (game["compteur"]//2 - 1) % 3
        promotion(game["plateau"], game["L_requete"][1], couleur, piece_type)
        game["plateau_pieces"], game["plateau_couleurs"] = afficher_plateau_sur_site(game["plateau"])
        envoyer_mise_a_jour(game_id)
        return jsonify({"reponse": f"Pion promu en {piece_type}"})
    
    if game["compteur_clic"] == 0:
        game["depart"] = value.lower()
        game["compteur_clic"] += 1
        return jsonify({"reponse": f"Case de départ sélectionnée: {value}"})
    elif game["compteur_clic"] == 1:
        arrivee = value.lower()
        depart = game["depart"]
        game["depart"] = None

        #  vérifie et fait le mouvement demandé s'il est légal
        if depart and arrivee:
            game["compteur_clic"] = 0
            if game["mode"]=="3joueurs":
                ok = tour_de_jeu_web(game["plateau"], (game["compteur_tour"])%3, depart, arrivee)
            elif game["mode"] == "ia_aleatoire":
                ok = tour_de_jeu_avec_IA_web(game["plateau"], depart, arrivee)
            elif game["mode"]=="ia_heuristique":
                ok = tour_de_jeu_IA_minimax_web_ou_on_dejoue(game["plateau"], depart, arrivee)
            if ok == False:
                print(depart, arrivee)
                return jsonify({"reponse": "Mouvement invalide"})
    if game["compteur_clic"] == 0:
        game["compteur_tour"] += 1
    game["plateau_pieces"], game["plateau_couleurs"] = afficher_plateau_sur_site(game["plateau"])
    envoyer_mise_a_jour(game_id)

    return jsonify({"reponse": value})


@socketio.on('connect')
def handle_connect():
    emit('update', {'message': 'Connexion établie'})

@socketio.on("join_game")
def join_game(data):
    game_id = data["game_id"]
    envoyer_mise_a_jour(game_id)


def envoyer_mise_a_jour(game_id):
    socketio.emit('update', {
        'game_id': game_id,
        'plateau_pieces': games[game_id]["plateau_pieces"],
        'plateau_couleurs': games[game_id]["plateau_couleurs"]
    })


if __name__ == '__main__':
    socketio.run(app, debug=True,allow_unsafe_werkzeug=True, host="0.0.0.0", port=5000)