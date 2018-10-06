from flask import jsonify, request
from db_interface.application import app, mysql


@app.route('/test')
def test():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM testdb.test;''')
    rv = cur.fetchall()
    return 'List of data in Test table in TestDB:\n' + str(rv)
