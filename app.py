import secrets
import sqlite3

import click
from flask import Flask, current_app, g

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

app.config['DATABASE'] = 'database.db'


# ---------------------------------Database---------------------------------------

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

app.teardown_appcontext

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    db.commit()

@click.command("init_db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

app.cli.add_command(init_db_command)

# ----------------------------------End-----------------------------------------------


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['nom']
        prenom = request.form['prenom']
        adresse = request.form['adresse']
        tel = request.form['tel']
        username = request.form['username']
        password = request.form['password']

        register_client_to_db(name, prenom, adresse, tel, username, password)
        return redirect(url_for('index'))
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if check_client(username, password):
            session['username'] = username

        return redirect(url_for('home'))
    else:
        redirect(url_for('index'))

@app.route('/home', methods=['GET'])
def home():
    return listOfProducts()

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)



# ----------------------------------Register client----------------------------------

def register_client_to_db(nom, prenom, adresse, tel, username, password):
    connection = get_db()
    cur = connection.cursor()
    cur.execute('INSERT INTO client(nom, prenom, adresse, tel, username, password) VALUES (?, ?, ?, ?, ?, ?)',
                (nom, prenom, adresse, tel, username, password))
    connection.commit()
    close_db()

# ---------------------------------Check client in database-----------------------------

def check_client(username, password):
    connection = get_db()
    cur = connection.cursor()
    cur.execute('SELECT username, password FROM client WHERE username=? AND password=?',
                (username, password))

    resultat = cur.fetchone()
    if resultat:
        return True
    else:
        return False