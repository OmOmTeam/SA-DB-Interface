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


@app.route('/create_parcel', methods=['POST', ])
def create_parcel():
    response = {'error': 'none'}

    if not request.is_json:
        response['error'] = 'JSON expected'
        return jsonify(response)

    try:
        j = request.get_json
        args = (j['order_id'], j['warehouse_id'],
                j['reciep_date'], j['height'],
                j['width'], j['depth'], j['weight'],
                )

        cur = mysql.connection.cursor()
        cur.execute('CALL LogisticCompany.CreateParcel', args)

        mysql.connection.commit()

    except KeyError:
        response['error'] = 'Invalid JSON'


@app.route('/get_parcel', methods=['GET', ])
def get_parcel():
    response = {'error': 'none'}

    try:
        cur = mysql.connection.cursor()

        args = (request.args['parcel_id'])
        cur.callproc('LogisticCompany.GetParcel', args)

        res = cur.fetchone()

        print(res)

        response['parcel'] = {
            'id': res[0],
            'status': res[1],
            'reciept_date': res[2],
            'arrival_date': res[3],
            'verify_code': res[4],
            'volume': res[5],
            'height': res[6],
            'width': res[7],
            'depth': res[8],
            'weight': res[9]

        }

    except KeyError:
        response['error'] = 'Invalid parameters'

    return jsonify(response)
