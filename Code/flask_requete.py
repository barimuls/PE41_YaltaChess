import uuid
from flask import Flask, request, jsonify, render_template, make_response
from Plateau import *
from flask_socketio import SocketIO, emit, join_room, leave_room
from FonctionJeux import *
from FonctionJeuxIA import *
import identification as id
import os
import jwt
from datetime import UTC, datetime, timedelta
import sqlite3
from collections import deque

lobby = deque()

dir = os.getcwd()
app = Flask(__name__)
socketio = SocketIO(app)
id.DATA_DIR = os.path.dirname(os.path.abspath(__file__))

with open("Code/secret_key.txt", "r", encoding="utf-8") as f:
    secret_key = f.read()

def nouvelle_partie(mode):
    plateau = creer_plateau()
    plateau.remplir_arete()
    #tutoriel
    cp = None # coup passant utilisé uniquement pour le tutoriel du coup en passant
    if len(mode) >= 9 and mode[:8] == 'tutoriel':
        if mode[9:] == 'tour':
            plateau.remplir_tutoriel_tour()
        elif mode[9:] == 'fou':
            plateau.remplir_tutoriel_fou()
        elif mode[9:] == 'cavalier':
            plateau.remplir_tutoriel_cavalier()
        elif mode[9:] == 'dame':
            plateau.remplir_tutoriel_dame()
        elif mode[9:] == 'pion':
            plateau.remplir_tutoriel_pion()
        elif mode[9:] == 'roi':
            plateau.remplir_tutoriel_roi()
        elif mode[9:] == 'roque':
            plateau.remplir_tutoriel_roque()
        elif mode[9:] == 'passant':
            plateau.remplir_tutoriel_passant()
            cp = True #True = 1er coup et False = tous les autres coups
    else:
        plateau.remplir_pieces_initiales()
    plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)

    return {
        "compteur_clic": 0, # Compteur servant à savoir si on est sur sélection départ ou arrivée
        "compteur_tour": 0, # Compteur servant à savoir quel joueur doit jouer
        "plateau": plateau,
        "plateau_pieces": plateau_pieces,
        "plateau_couleurs": plateau_couleurs,
        "mode": mode, # 3joueurs ou ia_min_min_max ou ia_aleatoire 
        "depart": None, # Case de départ sélectionnée
        "arrivee": None, # Case d'arrivée sélectionnée
        "coup_passant": cp # Utilisé uniquement pour le tutoriel du coup en passant
        }

def create_game(players):
    game_id = uuid.uuid4().hex[:8]
    games[game_id] = nouvelle_partie("multijoueur")
    games[game_id]["players"] = players # l'ensemble des joueurs de la partie
    games[game_id]["player"] = players[0] # le joueur dont c'est le tour (0, 1 ou 2)
    return game_id

def create_jwt(user_id):
    payload = {
        "sub": user_id,  # identifiant de l'utilisateur (UUID ou ID)
        "exp": datetime.now(UTC) + timedelta(hours=24)  # expiration dans 24h
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token

def verify_jwt(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload["sub"]  # retourne l'ID utilisateur
    except jwt.ExpiredSignatureError:
        return None  # token expiré
    except jwt.InvalidTokenError:
        return None  # token invalide
    
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

@app.route('/tutoriel/<game_id>')
def tutoriel(game_id):
    return render_template("tutoriel.html", game_id=game_id)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/user')
def user():
    return render_template("user.html")

# création d'une nouvelle partie et choix du mode
@app.route('/new_game', methods=['POST'])
def new_game():
    data = request.get_json()
    mode = data.get("mode", "reset")
    game_id = uuid.uuid4().hex[:8] # génere 64 caracteres aléatoires et selectionne les 8 premiers 
    games[game_id] = nouvelle_partie(mode)
    return jsonify({"game_id": game_id})

@app.route('/change_tutoriel/<game_id>', methods=['POST'])
def change_tutoriel(game_id):
    if game_id not in games:
        return jsonify({"error": "Partie inconnue"}), 404
    data = request.get_json()
    mode = data.get("mode", "reset")
    games[game_id] = nouvelle_partie(mode)
    envoyer_mise_a_jour(game_id)
    return jsonify({"reponse": "Tutoriel affiché"})

@app.route('/receive/depart/<game_id>', methods=['POST'])
def receive_depart(game_id):
    if game_id not in games:
        return jsonify({"error": "Partie inconnue"}), 404
    game = games[game_id]
    data = request.get_json()
    value = data.get('value')
    if game["mode"] == "multijoueur":
        game["player"] = data.get('player')
    game["depart"] = value.lower()
    game["compteur_clic"] += 1
    game["arrivee"] = None
    return jsonify({"reponse": f"Case de départ sélectionnée: {value}", "coup_possible": [game["plateau"].coup_possible(game["depart"])[i].upper() for i in range(len(game["plateau"].coup_possible(game["depart"])))]})

@app.route('/receive/arrivee/<game_id>', methods=['POST'])
def receive_arrivee(game_id):
    if game_id not in games:
        return jsonify({"error": "Partie inconnue"}), 404
    game = games[game_id]
    data = request.get_json()
    value = data.get('value')
    
    arrivee = value.lower()
    depart = game["depart"]
    game["depart"] = None
    game["arrivee"] = arrivee

    #  vérifie et fait le mouvement demandé s'il est légal
    if game["compteur_clic"] == 1 and depart and arrivee:
        game["compteur_clic"] = 0
        if game["mode"]=="3joueurs":
            ok = tour_de_jeu_web(game["plateau"], (game["compteur_tour"])%3, depart, arrivee)
        elif game["mode"] == "ia_aleatoire":
            ok = tour_de_jeu_avec_IA_web(game["plateau"], depart, arrivee)
        elif game["mode"]=="ia_min_min_max":
            #ok = tour_de_jeu_IA_minimax_web_ou_on_dejoue(game["plateau"], depart, arrivee)
            ok = tour_de_jeu_test(game["plateau"], depart, arrivee) 
        elif len(game["mode"]) >=8 and game["mode"][:8]=="tutoriel":
            if game["mode"][9:] == "passant":
                if game["coup_passant"] == True:
                    ok = tour_de_jeu_web(game["plateau"], 0, depart, arrivee)
                    jouer_le_coup(game["plateau"], 1, 'i7', 'i5')
                    game["coup_passant"] = False
                else:
                    ok = tour_de_jeu_web(game["plateau"], 0, depart, arrivee)
            else:
                ok = tour_de_jeu_web(game["plateau"], 0, depart, arrivee)
        elif game["mode"] == "multijoueur":
            ok = tour_de_jeu_web(game["plateau"], game["players"].index(game["player"]), depart, arrivee)
            game["player"] = game["players"][(game["players"].index(game["player"])+1)%3] # passe au joueur suivant
        elif game["mode"] == "test":
             pass #à implémenter pour mesurer le temps de calcul de chaque IA
        if ok == False:
            print(depart, arrivee)
            return jsonify({"reponse": "Mouvement invalide"})
    if game["compteur_clic"] == 0:
        game["compteur_tour"] += 1
    game["plateau_pieces"], game["plateau_couleurs"] = afficher_plateau_sur_site(game["plateau"])
    envoyer_mise_a_jour(game_id)
    if verifier_victoire(game["plateau"]):
        return jsonify({"reponse": f"Victoire du joueur {(game['compteur_tour']-1)%3 + 1}", 'plateau_pieces': game["plateau_pieces"]})
    return jsonify({"reponse": value})

@app.route('/receive/promotion/<game_id>', methods=['POST'])
def receive_promotion(game_id):
    if game_id not in games:
        return jsonify({"error": "Partie inconnue"}), 404
    game = games[game_id]
    data = request.get_json()
    value = data.get('value')
    # PROMOTION
    if game["mode"] == "3joueurs":
        couleur = (game["compteur_tour"]+2) % 3
    elif game["mode"] == "multijoueur":
        couleur = game["players"].index(game["player"])
    else:
        couleur = 0
    promotion(game["plateau"], game["arrivee"], couleur, value)
    game["plateau_pieces"], game["plateau_couleurs"] = afficher_plateau_sur_site(game["plateau"])
    envoyer_mise_a_jour(game_id)
    return jsonify({"reponse": f"Pion promu en {value}"})

@app.route('/receive/reset/<game_id>', methods=['POST'])
def receive_reset(game_id):
    if game_id not in games:
        return jsonify({"error": "Partie inconnue"}), 404
    game = games[game_id]
    data = request.get_json()
    value = data.get('value')

    # RESET la partie dans le meme mode avec le meme identifiant
    games[game_id] = nouvelle_partie(game["mode"])
    envoyer_mise_a_jour(game_id)
    return jsonify({"reponse": "Partie réinitialisée", 'plateau_pieces': game["plateau_pieces"]})

@app.route('/auth/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    if not username or not password or not confirm_password:
        return jsonify({"reponse": "Champs manquants"}), 400
    player_id = id.register(username, password, confirm_password)
    if not player_id:
        return jsonify({"reponse": "Identifiant déjà utilisé"}), 409
    token = create_jwt(player_id)
    response = make_response(jsonify({"reponse": "Utilisateur enregistré", "user_id": player_id}))
    response.set_cookie("token", token, httponly=True, samesite="Lax", max_age=3600*24)
    return response, 200

@app.route('/auth/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"reponse": "Champs manquants"}), 400
    player_id = id.login(username, password)
    if not player_id:
        return jsonify({"reponse": "Identifiant ou mot de passe incorrect"}), 401
    token = create_jwt(player_id)
    response = make_response(jsonify({"reponse": "Connexion réussie", "user_id": player_id}))
    response.set_cookie("token", token, httponly=True, samesite="Lax", max_age=3600*24)
    return response, 200

@app.route('/auth/me')
def me():
    token = request.cookies.get("token")
    if not token:
        return jsonify({"loggedIn": False}), 200
    user_id = verify_jwt(token)
    if not user_id:
        return jsonify({"loggedIn": False}), 200
    conn = sqlite3.connect(f"{id.DATA_DIR}/user_database.sqlite")
    cursor = conn.cursor()
    stored_user = cursor.execute("""SELECT user_id FROM user_table WHERE user_uuid = ?""", (user_id,)).fetchone()
    conn.close()
    return jsonify({"loggedIn": True, "user_id": user_id, "username": stored_user[0]}), 200

@app.route('/auth/logout')
def logout():
    response = jsonify({"success": True})
    response.set_cookie("token", "", expires=0)
    return response

@app.route('/lobby/join', methods=['POST'])
def join_lobby():
    global lobby
    user_id = request.json.get("user_id")
    # éviter les doublons
    if user_id not in lobby:
        lobby.append(user_id)
    # si on a 3 joueurs → créer une partie
    if len(lobby) >= 3:
        players = [lobby.popleft(), lobby.popleft(), lobby.popleft()]
        game_id = create_game(players)
        for p in players:
            socketio.emit("matched", {"game_id": game_id}, room=p)
        return jsonify({"status": "matched", "game_id": game_id, "players": players})
    return jsonify({"status": "waiting", "position": len(lobby)})

@app.route('/game/search_player/<game_id>', methods=['POST'])
def search_player(game_id):
    if games[game_id]["mode"] != "multijoueur":
        return None
    token = request.cookies.get("token")
    if not token:
        return jsonify({"loggedIn": False}), 200
    user_id = verify_jwt(token)

    if game_id not in games:
        return None
    game = games[game_id]
    for i, p in enumerate(game["players"]):
        if p == user_id:

            return jsonify({"player_index": ['blanc','rouge','noir'][i]}), 200
    return None


@socketio.on('connect')
def handle_connect():
    emit('update', {'message': 'Connexion établie'})

@socketio.on("join_game")
def join_game(data):
    game_id = data["game_id"]
    join_room(game_id)
    envoyer_mise_a_jour(game_id)

@socketio.on("register")
def register(data):
    user_id = data["user_id"]
    join_room(user_id)
    print(f"Joueur {user_id} a rejoint sa room Socket.IO")


def envoyer_mise_a_jour(game_id):
    if games[game_id]["mode"] == "3joueurs":
        joueur = (games[game_id]["compteur_tour"])%3
    elif games[game_id]["mode"] == "multijoueur":
        joueur = games[game_id]["player"]
        print("Joueur actuel:", joueur)
    else:
        joueur = 0
    socketio.emit('update', {'game_id': game_id, 'plateau_pieces': games[game_id]["plateau_pieces"], 'plateau_couleurs': games[game_id]["plateau_couleurs"], 'joueur' : joueur, 'mode': games[game_id]["mode"]}, room=game_id)

if __name__ == '__main__':
    socketio.run(app, debug=True,allow_unsafe_werkzeug=True, host="0.0.0.0", port=5000)