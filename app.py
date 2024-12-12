from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        song = request.form.get('song')
        flash(f'Música "{song}" registrada com sucesso!', 'success')
        return redirect(url_for('registrar'))
    return render_template('registrar.html')

if __name__ == '__main__':
    app.run(debug=True)
