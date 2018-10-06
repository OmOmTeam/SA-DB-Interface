import db_interface.config

from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object("db_interface.config.DevelopConfig")

mysql = MySQL(app)
