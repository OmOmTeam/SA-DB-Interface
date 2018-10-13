from flask import jsonify, request
from db_interface.application import app, mysql

"""
    response = {'error': 'none'}
    if request.is_json:
        pass

    else:
        response['error'] = 'JSON expected'

    return jsonify(response)
"""


@app.route('/register_new_employee', methods=['POST', ])
def register_new_employee():
    response = {'error': 'none'}

    if not request.is_json:
        response['error'] = 'JSON expected'
        return jsonify(response)

    try:
        j = request.get_json()

        cur = mysql.connection.cursor()

        args = (j['login'], j['password'], j['role'])
        cur.callproc('LogisticCompany.Registration', args)

    except KeyError:
        response['error'] = 'Invalid JSON'

    return jsonify(response)


@app.route('/get_access_rights', methods=['GET', ])
def get_access_rights():
    cur = mysql.connection.cursor()

    args = ('Admin', 'admin', 0)
    cur.callproc('LogisticCompany.GetAccessRights', args)
    cur.execute('SELECT @_LogisticCompany.GetAccessRights_2')

    res = cur.fetchone()

    return str(res[0])
