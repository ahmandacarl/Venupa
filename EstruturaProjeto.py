from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = "segredo_Venupas"

# Lista simulando o banco de dados
produtos = []



@app.route('/')
def index():
    return render_template('index.html', produtos=produtos)


@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        descricao = request.form['descricao']
        imagem = request.files['imagem']

        if imagem:
            filename = secure_filename(imagem.filename)
            caminho = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagem.save(caminho)
        else:
            caminho = None

        produtos.append({
            'id': len(produtos) + 1,
            'nome': nome,
            'preco': preco,
            'descricao': descricao,
            'imagem': caminho
        })

        return redirect(url_for('index'))

    return render_template('adicionar.html')


@app.route('/produto/<int:id>')
def produto(id):
    item = next((p for p in produtos if p['id'] == id), None)
    return render_template('produto.html', produto=item)


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
