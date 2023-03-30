import secrets
import sqlite3
from winreg import HKEY_CURRENT_USER

import click
from flask import (
    Flask,
    current_app,
    g,
    jsonify,
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
    cur.execute("SELECT * from PRODUCT")
    results = cur.fetchall()

    return results


# ---list Products Of Customer-------


def listProductsOfCustomer(customer_id):
    connexion = get_db()
    cur = connexion.cursor()
    cur.execute(
        """SELECT p.libelle, p.price, pc.quantity 
                   FROM customer c
                   INNER JOIN command cmd ON c.idcustomer = cmd.idcustomer
                   INNER JOIN product_command pc ON cmd.idcommand = pc.idcommand
                   INNER JOIN product p ON pc.idProduct = p.idProduct
                   WHERE c.idcustomer = ?;""",
        (customer_id,),
    )
    productsOfCustomer = cur.fetchall()
    return productsOfCustomer


@app.route("/commander", methods=["POST"])
def commander():
    # Récupération des données de la commande envoyées dans la requête POST
    id_product = request.json["id_product"]
    quantity = request.json["quantity"]
    id_customer = request.json["id_customer"]

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO command (idcustomer, commanddate) VALUES (?, date('now'))",
            (id_customer,),
        )
        id_command = cursor.lastrowid

        cursor.execute(
            "INSERT INTO product_command (idcommand, idProduct, quantity) VALUES (?, ?, ?)",
            (id_command, id_product, quantity),
        )

        conn.commit()

        conn.close()

        return jsonify({"status": "success"})

    except Exception as e:
        # En cas d'erreur, annulation de la transaction et retour d'un message d'erreur
        conn.rollback()
        conn.close()
    # return jsonify({'status': 'error', 'message': str(e)})


# ----------------------------------root-----------------------------------------------


@app.route("/")
def index():
    products = listOfProducts()
    if "username" in session:
        username = session["username"]
    else:
        username = None

    products = listOfProducts()

    return render_template("index.html", products=products, username=username)


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


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/forgetpassword")
def forgetpassword():
    return render_template("forgetpassword.html")


# CART


@app.route("/process_cart", methods=["POST"])
def process_cart():
    cart_data = request.get_json()
    total = 0
    for item in cart_data:
        total += item["price"] * item["quantity"]

    session["cart_data"] = cart_data
    session["total"] = total

    return jsonify({"url": url_for("paiement")})


@app.route("/paiement")
def paiement():
    cart_data = session.get("cart_data", [])
    total = session.get("total", 0)
    return render_template("paiement.html", cart_data=cart_data, total=total)


if __name__ == "__main__":
    app.run(debug=True)
