import secrets
import sqlite3
from winreg import HKEY_CURRENT_USER

import click
from flask import (Flask, current_app, g, jsonify, redirect, render_template,
                   request, session, url_for)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

app.config["DATABASE"] = "database.db"


# ---------------------------------Database---------------------------------------

# Connection to the database
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


app.teardown_appcontext

# Closing the database
def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

# Initialize the database
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
        "SELECT idcustomer, username, password FROM customer WHERE username=? AND password=?",
        (username, password),
    )

    resultat = cur.fetchone()
    if resultat:
        session["id_Customer"] = resultat[0]
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


def listProductsOfCustomer():
    connexion = get_db()
    cur = connexion.cursor()
    cur.execute(
        """SELECT p.libelle, p.price, pc.quantity 
                   FROM customer c
                   INNER JOIN command cmd ON c.idcustomer = cmd.idcustomer
                   INNER JOIN product_command pc ON cmd.idcommand = pc.idcommand
                   INNER JOIN product p ON pc.idProduct = p.idProduct
                   WHERE c.idcustomer = ?;""",
        (session.get("id_Customer"),),
    )
    productsOfCustomer = cur.fetchall()
    return productsOfCustomer


@app.route("/payer", methods=["POST"])
def commander():
    id_customer = session.get("id_Customer")
    quantity = 1
    product_ids = session.get("product_ids")
    print(id_customer)
    print(product_ids)

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO command (idcustomer, commanddate) VALUES (?, date('now'))",
            (id_customer,),
        )
        id_command = cursor.lastrowid

        for id_product in product_ids:
            cursor.execute(
                "INSERT INTO product_command (idcommand, idProduct, quantity) VALUES (?, ?, ?)",
                (id_command, id_product, quantity),
            )

        conn.commit()

        conn.close()

        return jsonify({"status": "success"})

    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"status": "error", "message": str(e)})


# ----------------------------------root-----------------------------------------------


@app.route("/")
def index():
    products = listOfProducts()
    productsOfCustomer = None
    number = 0
    print(productsOfCustomer)
    if "username" in session:
        username = session["username"]
        productsOfCustomer = listProductsOfCustomer()
        number = len(productsOfCustomer)

    else:
        username = None

    products = listOfProducts()

    search_query = request.args.get("search_query")
    if search_query:
        products = [
            product
            for product in products
            if search_query.lower() in product[2].lower()
        ]

    return render_template(
        "index.html",
        products=products,
        username=username,
        productsOfCustomer=productsOfCustomer,
        number=number,
    )


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

# Log out
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/forgetpassword", methods=["GET", "POST"])
def forgetpassword():
    if request.method == "POST":
        username = request.form["username"]
        new_password = request.form["new_password"]
        
        connection = get_db()
        cur = connection.cursor()
        
        # Mettre à jour le mot de passe dans la base de données pour l'utilisateur avec le nom d'utilisateur donné
        cur.execute(
            "UPDATE customer SET password = ? WHERE username = ?",
            (new_password, username),
        )
        connection.commit()
        
        # Rediriger l'utilisateur vers la page de connexion après avoir mis à jour le mot de passe
        return redirect(url_for("index"))
    else:
        return render_template("forgetpassword.html")


# CART


@app.route("/process_cart", methods=["POST"])
def process_cart():
    cart_data = request.get_json()
    total = 0
    product_ids = []
    for item in cart_data:
        total += item["price"] * item["quantity"]
        product_ids.append(item["productId"])

    session["cart_data"] = cart_data
    session["total"] = total
    session["product_ids"] = product_ids
    return jsonify({"url": url_for("paiement")})


@app.route("/paiement")
def paiement():
    cart_data = session.get("cart_data", [])
    total = session.get("total", 0)
    product_ids = session.get("product_ids")

    return render_template(
        "paiement.html",
        cart_data=cart_data,
        total=total,
        product_ids=product_ids,
    )


if __name__ == "__main__":
    app.run(debug=True)
