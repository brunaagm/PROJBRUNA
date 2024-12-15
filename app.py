from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from functools import wraps

# Inicializa o aplicativo Flask
app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Usar uma chave secreta para sessões

# Configuração do banco de dados (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///songs.db'  # Caminho do banco de dados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa a modificação de rastreamento de objetos

# Inicializa o banco de dados
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelo de Musica
class Musica(db.Model):
    __tablename__ = 'musicas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)  # Nome da música
    cantor = db.Column(db.String(120), nullable=False)  # Nome do cantor

    def __repr__(self):
        return f'<Musica {self.nome} - {self.cantor}>'

# Modelo de Usuario
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    senha = db.Column(db.String(200), nullable=False)

# Middleware para verificar se o usuário está autenticado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):  # Verifica se o usuário está logado
            flash('Você precisa estar logado para acessar essa página.', 'warning')
            return redirect(url_for('login'))  # Redireciona para a página de login
        return f(*args, **kwargs)
    return decorated_function

# Página de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('registrar'))

    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        print(f"Recebendo login: usuário={usuario}, senha={senha}")  # Debug

        if usuario == 'ex@gmail.com' and senha == 'senha123':  # Mock de credenciais
            session['logged_in'] = True
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('registrar'))
        else:
            flash('Credenciais inválidas', 'error')

    return render_template('login.html')

# Página de registro de músicas
@app.route('/registrar', methods=['GET', 'POST'])
@login_required
def registrar():
    if request.method == 'POST':
        musica_name = request.form.get('song_name')
        cantor = request.form.get('cantor_name')

        if musica_name and cantor:
            new_song = Musica(nome=musica_name, cantor=cantor)
            db.session.add(new_song)
            db.session.commit()
            flash('Música registrada com sucesso!', 'success')
        else:
            flash('Por favor, preencha todos os campos.', 'error')

    songs = Musica.query.all()
    return render_template('registrar.html', songs=songs)

# Rota de logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Você foi deslogado.', 'info')
    return redirect(url_for('login'))

# Rota para excluir uma música
@app.route('/excluir/<int:id>')
@login_required
def excluir_musica(id):
    song_to_delete = Musica.query.get(id)
    if song_to_delete:
        db.session.delete(song_to_delete)
        db.session.commit()
        flash('Música excluída com sucesso.', 'success')
    else:
        flash('Música não encontrada.', 'error')
    return redirect(url_for('registrar'))

# Inicialização do banco de dados
@app.before_request
def before_request():
    with app.app_context():
        db.create_all()  # Garante que as tabelas existem antes da primeira requisição

if __name__ == '__main__':
    app.run(debug=True)
