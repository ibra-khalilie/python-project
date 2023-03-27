import secrets
import sqlite3

import click
from flask import (Flask, current_app, g, redirect, render_template, request,
                   session, url_for)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

app.config['DATABASE'] = 'database.db'

