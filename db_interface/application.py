import db_interface.config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object("db_interface.config.DevelopConfig")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
