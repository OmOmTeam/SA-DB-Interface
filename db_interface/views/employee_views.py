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


@app.route('/login', methods=['POST', ])
def login():
    response = {'error': 'none'}

    if not request.is_json:
        response['error'] = 'JSON expected'
        return jsonify(response)

    try:
        j = request.get_json()
        login, passhash = j['login'], j['password_hash']

        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT idEmployees, idAccessRights
            FROM LogisticCompany.Employees
            WHERE Login = %s AND PassHash = %s;
            """, (login, passhash,))

        employee_id, access_rights = cur.fetchone()

        if employee_id:
            response['access_right_id'] = access_rights

        else:
            response['error'] = 'Invalid Login or Password'

    except KeyError:
        response['error'] = 'Invalid JSON'

    return jsonify(response)


@app.route('/user_by_login', methods=['GET', ])
def user_by_login():
    response = {'error': 'none'}

    try:
        login = request.args['login']

        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT Login,PassHash,idAccessRights
            FROM LogisticCompany.Employees
            WHERE Login = %s;
            """, (login, ))

        res = cur.fetchone()
        print(res)
        login, passhash, idar = res
        response['login'] = login
        response['password_hash'] = passhash
        response['access_rights_id'] = idar

    except KeyError:
        response['error'] = 'Invalid parameters'

    return jsonify(response)


@app.route('/register_new_employee', methods=['POST', ])
def register_new_employee():
    response = {'error': 'none'}

    if not request.is_json:
        response['error'] = 'JSON expected'
        return jsonify(response)

    try:
        j = request.get_json()

        cur = mysql.connection.cursor()

        args = (0, j['login'], j['password_hash'], j['role'])
        cur.callproc('LogisticCompany.RegisterEmployee', args)
        cur.execute('SELECT @_LogisticCompany.RegisterEmployee_0')

        response['employee_id'] = cur.fetchone()[0]

        mysql.connection.commit()

    except KeyError:
        response['error'] = 'Invalid JSON'

    return jsonify(response)


@app.route('/get_access_rights', methods=['GET', ])
def get_access_rights():
    response = {'error': 'none'}

    try:

        cur = mysql.connection.cursor()

        args = (request.args['login'], request.args['password_hash'], 0)
        cur.callproc('LogisticCompany.GetAccessRights', args)
        cur.execute('SELECT @_LogisticCompany.GetAccessRights_2')

        res = cur.fetchone()

        response['access_rights'] = res[0]

    except KeyError:
        response['error'] = 'Invalid parameters'

    return jsonify(response)


@app.route('/register_customer', methods=['POST', ])
def register_customer():
    response = {'error': 'none'}

    if not request.is_json:
        response['error'] = 'JSON expected'
        return jsonify(response)

    try:
        j = request.get_json()

        cur = mysql.connection.cursor()

        args = (j['login'], j['password_hash'])
        cur.callproc('LogisticCompany.RegisterCustomer', args)

        mysql.connection.commit()

    except KeyError:
        response['error'] = 'Invalid JSON'

    return jsonify(response)
