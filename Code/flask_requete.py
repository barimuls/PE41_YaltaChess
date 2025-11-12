from flask import Flask, request, jsonify, render_template
from Plateau import *

app = Flask(__name__)
compteur = 0
L_requete = [0,0]
plateau = creer_plateau()
plateau.remplir_arete()
plateau.remplir_pieces_initiales()
plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)

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
    global compteur, L_requete, plateau_pieces, plateau_couleurs, plateau
    data = request.get_json()
    value = data.get('value')
    L_requete[compteur%2] = value.lower()
    print(f"Valeur reçue : {value}")
    print(compteur)
    depart = L_requete[0]
    arrivee = L_requete[1]
    if compteur % 2 == 1:
        if tour_de_jeu_web(plateau,(compteur//2)%3, depart, arrivee)==False:
            return jsonify({"reponse": "Mouvement invalide"})
    compteur += 1
    plateau_pieces, plateau_couleurs = afficher_plateau_sur_site(plateau)
    return jsonify({"reponse": value})


if __name__ == '__main__':
    app.run(debug=True)
