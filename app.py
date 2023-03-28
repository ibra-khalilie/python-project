import secrets
import sqlite3

import click
from flask import (
    Flask,
    current_app,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

app.config["DATABASE"] = "database.db"


# ---------------------------------Database---------------------------------------


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


app.teardown_appcontext


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))
    db.commit()


@click.command("init_db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


app.cli.add_command(init_db_command)

# ----------------------------------End-----------------------------------------------


# ----------------------------------Register client----------------------------------


def register_client_to_db(name, firstname, adress, phone, username, password):
    connection = get_db()
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO customer(name, firstname, adress, phone, username, password) VALUES (?, ?, ?, ?, ?, ?)",
        (name, firstname, adress, phone, username, password),
    )
    connection.commit()
    close_db()


# ---------------------------------Check client in database-----------------------------


def check_client(username, password):
    connection = get_db()
    cur = connection.cursor()
    cur.execute(
        "SELECT username, password FROM customer WHERE username=? AND password=?",
        (username, password),
    )

    resultat = cur.fetchone()
    if resultat:
        return True
    else:
        return False


# ------list of product----


def listOfProducts():
    connection = get_db()
    cur = connection.cursor()
    cur.execute("SELECT libelle,image,price from PRODUCT")
    results = cur.fetchall()

    return results


# ----------------------------------root-----------------------------------------------


@app.route("/")
def index():
    products = listOfProducts()
    return render_template("index.html", products=products)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        firstname = request.form["firstname"]
        adress = request.form["adress"]
        phone = request.form["phone"]
        username = request.form["username"]
        password = request.form["password"]

        register_client_to_db(name, firstname, adress, phone, username, password)
        return redirect(url_for("index"))
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if check_client(username, password):
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return render_template(
                "login.html", error="Identifiant or Password is wrong!"
            )
    else:
        return render_template("login.html")


@app.route("/home", methods=["GET", "POST"])
def home():
    if "username" in session:
        return redirect(url_for("index"))
    else:
        return "Identifiant or Password is wrond!"


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
