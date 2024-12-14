from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Inicializa o aplicativo Flask
app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Configuração do banco de dados (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///songs.db'  # Caminho do banco de dados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa a modificação de rastreamento de objetos

# Inicializa o banco de dados
db = SQLAlchemy(app)

# Inicializa o Flask-Migrate
migrate = Migrate(app, db)

# Definindo o modelo de dados para a tabela 'Musica'
class Musica(db.Model):
    __tablename__ = 'musicas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)  # Nome da música
    cantor = db.Column(db.String(120), nullable=False)  # Nome do cantor

    def __repr__(self):
        return f'<Musica {self.nome} - {self.cantor}>'

# Função para criar as tabelas no banco de dados (executar isso se necessário)
def create_tables():
    with app.app_context():
        db.create_all()  # Criação das tabelas

# Página de login
@app.route('/')
def login():
    return render_template('login.html')

# Página de registro de músicas e listagem das músicas
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        musica_name = request.form.get('song_name')  # Correspondência com o nome do campo no HTML
        cantor = request.form.get('cantor_name')

        if musica_name and cantor:
            # Criar uma nova instância de Musica e adicionar ao banco
            new_song = Musica(nome=musica_name, cantor=cantor)
            db.session.add(new_song)  # Adiciona a música à sessão
            db.session.commit()  # Confirma a adição ao banco

            songs = Musica.query.all()  # Recupera todas as músicas
            flash('Dados registrados com sucesso!', 'success')

            for song in songs:
                print(f'{song.nome} - {song.cantor}')  # Imprime as músicas no console

        else:
            flash('Por favor, insira os dados.', 'error')

    songs = Musica.query.all()  # Recupera todas as músicas
    return render_template('registrar.html', songs=songs)

# Rota para excluir uma música
@app.route('/excluir/<int:id>')
def excluir_musica(id):
    song_to_delete = Musica.query.get(id)
    if song_to_delete:
        db.session.delete(song_to_delete)
        db.session.commit()
    return redirect(url_for('registrar'))

# Executar o aplicativo
if __name__ == '__main__':
    create_tables()  # Garantir que as tabelas sejam criadas no início
    app.run(debug=True)
