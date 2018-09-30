from flask import jsonify, request
from db_interface.application import app


@app.route('/')
def index():
    return 'Hello, world!'
