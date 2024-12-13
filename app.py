from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Configuração do banco de dados (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///songs.db'  # Caminho do banco de dados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa a modificação de rastreamento de objetos
db = SQLAlchemy(app)

# Definindo o modelo de dados para a tabela 'Song'
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Song {self.name}>'

# Criação do banco de dados (isso só precisa ser feito uma vez)
def create_tables():
    with app.app_context():
        db.create_all()

# Página de login
@app.route('/')
def login():
    return render_template('login.html')

# Página de registro de músicas
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        song_name = request.form.get('song')
        if song_name:
            # Criar uma nova instância de Song e adicionar ao banco
            new_song = Song(name=song_name)
            db.session.add(new_song)  # Adiciona a música à sessão
            db.session.commit()  # Confirma a adição ao banco
            flash(f'Música "{song_name}" registrada com sucesso!', 'success')
        else:
            flash('Por favor, insira o nome da música.', 'error')

    # Recupera todas as músicas cadastradas e exibe
    songs = Song.query.all()  # Recupera todas as músicas
    return render_template('registrar.html', songs=songs)

# Rota para listar as músicas
@app.route('/listar')
def listar():
    songs = Song.query.all()  # Obtém todas as músicas do banco
    return render_template('listar.html', songs=songs)

# Chama a criação da tabela de músicas quando a aplicação iniciar
create_tables()

if __name__ == '__main__':
    app.run(debug=True)
