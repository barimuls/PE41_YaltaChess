from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>EXEMPLE, JE SUIS EN TRAIN DE FAIRE DES TESTS !!</title>
</head>
<body>
    <h1>Interface Flask</h1>
    <form method="POST">
        <label>Entrez un texte :</label>
        <input type="text" name="texte" required>
        <button type="submit">Valider</button>
    </form>
    {% if texte %}
        <p>Vous avez écrit : {{ texte }}</p>
    {% endif %}
</body>
</html>
'''


@app.route('/', methods=['GET', 'POST'])
def index():
    texte = None
    if request.method == 'POST':
        texte = request.form['texte']
    return render_template_string(HTML, texte=texte)


if __name__ == '__main__':
    app.run(debug=True)
