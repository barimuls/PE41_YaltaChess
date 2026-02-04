import uuid
from flask import Flask, request, jsonify, render_template
from Plateau import *
from flask_socketio import SocketIO, emit
from FonctionJeux import *

app = Flask(__name__)
socketio = SocketIO(app)

def nouvelle_partie(mode):
    plateau = creer_plateau()
    plateau.remplir_arete()
    plateau.remplir_pieces_initiales()
    plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)

    return {
        "compteur": 0,
        "L_requete": [None, None],
        "plateau": plateau,
        "plateau_pieces": plateau_pieces,
        "plateau_couleurs": plateau_couleurs,
        "n_ligne": (mode == "3joueurs"),
        "type_ia": mode if mode.startswith("ia") else None,
        "mode": mode
    }

games = {}


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


@app.route('/jeu/<game_id>')
def jeu(game_id):
    return render_template("jeu.html", game_id=game_id)

@app.route('/new_game', methods=['POST'])
def new_game():
    data = request.get_json()
    mode = data.get("mode", "reset")
    game_id = uuid.uuid4().hex[:8]
    games[game_id] = nouvelle_partie(mode)
    return jsonify({"game_id": game_id})

@app.route('/receive/<game_id>', methods=['POST'])
def receive(game_id):
    if game_id not in games:
        return jsonify({"error": "Partie inconnue"}), 404
    game = games[game_id]
    data = request.get_json()
    value = data.get('value')

    envoyer_mise_a_jour(game_id)

    # RESET
    if value == 'reset':
        games[game_id] = nouvelle_partie(game["mode"])
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
        couleur = 0 if not game["n_ligne"] else (game["compteur"]//2 - 1) % 3
        promotion(game["plateau"], game["L_requete"][1], couleur, piece_type)
        game["plateau_pieces"], game["plateau_couleurs"] = afficher_plateau_sur_site(game["plateau"])
        return jsonify({"reponse": f"Pion promu en {piece_type}"})

    # MOUVEMENT
    game["L_requete"][game["compteur"] % 2] = value.lower()
    depart, arrivee = game["L_requete"]
    if game["compteur"] % 2 == 1 and depart and arrivee:
        if game["n_ligne"]:
            ok = tour_de_jeu_web(game["plateau"], (game["compteur"]//2)%3, depart, arrivee)
        else:
            if game["type_ia"] == "ia_aleatoire":
                ok = tour_de_jeu_avec_IA_web(game["plateau"], depart, arrivee)
            else:
                ok = tour_de_jeu_IA_minimax_web_ou_on_dejoue(game["plateau"], depart, arrivee)
        if not ok:
            game["compteur"] -= 1
            return jsonify({"reponse": "Mouvement invalide"})
    game["compteur"] += 1
    game["plateau_pieces"], game["plateau_couleurs"] = afficher_plateau_sur_site(game["plateau"])
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