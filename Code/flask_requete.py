from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

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
    data = request.get_json()
    value = data.get('value')
    print(f"Valeur reçue : {value}")
    return jsonify({"reponse": value})


if __name__ == '__main__':
    app.run(debug=True)
    