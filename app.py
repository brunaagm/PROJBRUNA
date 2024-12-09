from flask import flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/novo'  # Pode ser MySQL, PostgreSQL etc.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        db.init_app(app)
        db.create_all()

app = Flask(__name__)


USUARIOS = {
    "usuario": "senhabrunalinda"
}

@app.route('/', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
       
        if username in USUARIOS and USUARIOS[username] == password:
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Usuário ou senha inválidos.")
    
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return "Bem-vindo!"

if __name__ == '__main__':
    app.run(debug=True)
