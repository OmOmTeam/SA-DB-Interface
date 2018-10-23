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


@app.route('/add_address', methods=['POST', ])
def add_address():
    response = {'error': 'none'}

    if not request.is_json:
        response['error'] = 'JSON expected'
        return jsonify(response)

    try:
        cur = mysql.connection.cursor()
        request_json = request.get_json()

        args = (request_json['country'],
                request_json['region'],
                request_json['city'],
                request_json['street'],
                request_json['building'],
                request_json['addition_info'],
                0)

        cur.callproc('LogisticCompany.AddAddress', args)
        cur.execute('SELECT @_LogisticCompany.AddAddress_6')

        response['address_id'] = cur.fetchone()[0]

        mysql.connection.commit()

    except KeyError:
        response['error'] = 'Invalid JSON'
        return jsonify(response)

    return jsonify(response)


@app.route('/add_warehouse', methods=['POST', ])
def add_warehouse():
    response = {'error': 'none'}

    if not request.is_json:
        response['error'] = 'JSON expected'
        return jsonify(response)

    try:
        cur = mysql.connection.cursor()
        request_json = request.get_json()

        args = (0, request_json['capacity'], request_json['country'],
                request_json['region'], request_json['city'],
                request_json['street'], request_json['building'],
                request_json['additional_info']
                )

        cur.callproc('LogisticCompany.AddWarehouse', args)
        cur.execute('SELECT @_LogisticCompany.AddWarehouse_0')

        response['warehouse_id'] = cur.fetchone()[0]

        mysql.connection.commit()

    except KeyError:
        response['error'] = 'Invalid JSON'
        return jsonify(response)

    return jsonify(response)


@app.route('/get_warehouses', methods=['GET'])
def get_warehouses():
    response = {'error': 'none', 'warehouses': []}

    cur = mysql.connection.cursor()

    cur.callproc('LogisticCompany.GetWareHouses')

    for row in cur.fetchall():
        response['warehouses'].append({
            'id': row[0],
            'capacity': row[1],
            'current_load': row[2],
            'country': row[3],
            'region': row[4],
            'city': row[5],
            'street': row[6],
            'building': row[7],
            'additional_info': row[8]
            })

    return jsonify(response)
