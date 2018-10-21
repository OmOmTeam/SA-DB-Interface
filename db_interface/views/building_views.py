from flask import jsonify, request
from db_interface.application import app, mysql

"""
@app.route('/test')
def test():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM testdb.test;''')
    rv = cur.fetchall()
    return 'List of data in Test table in TestDB:\n' + str(rv)
"""


@app.route('/add_warehouse', methods=['POST', ])
def add_warehouse():
    response = {'error': 'none'}

    if not request.is_json:
        response['error'] = 'JSON expected'
        return jsonify(response)

    try:
        cur = mysql.connection.cursor()
        request_json = request.get_json()

        args = (0, request_json['capacity'], request_json['country'], request_json['region'], request_json['city'],
                request_json['street'], request_json['buildingNum'], request_json['additionalInfo'])

        cur.callproc('LogisticCompany.AddWarehouse', args)
        cur.execute("SELECT @_LogisticCompany.AddWarehouse_0")

        response['warehouse_id'] = cur.fetchone()[0]

        mysql.connection.commit()
        cur.close()

    except KeyError:
        response['error'] = 'Invalid JSON'
        return jsonify(response)

    return jsonify(response)
