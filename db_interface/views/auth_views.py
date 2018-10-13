from flask import jsonify, request
from db_interface.application import app, mysql


@app.route('/get_access_rights')
def get_access_rights():
    cur = mysql.connection.cursor()

    args = ['Admin', 'admin']
    cur.callproc('GetAccessRights', args)

    res = ''

    for result in cur.stored_results():
        res += result.fetchall()

    return str(res)
