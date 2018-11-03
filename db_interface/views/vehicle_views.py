from flask import jsonify, request
from db_interface.application import app, mysql
import requests

"""
@app.route('/test')
def test():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM testdb.test;''')
    rv = cur.fetchall()
    return 'List of data in Test table in TestDB:\n' + str(rv)
"""


@app.route('/update_vehicle_location', methods=['POST', ])
def update_vehicle_location():
    response = {'error': 'none'}

    if request.is_json:
        response['error'] = 'JSON expected'
        return jsonify(response)

    try:
        j = request.get_json()
        vehicle_id = j['vehicle_id']
        latitude = j['latitude']
        longitude = j['longitude']

        cur = mysql.connection.cursor()
        cur.execute('''SELECT idLocation
                    FROM LogisticCompany.Vehicle
                    WHERE idVehicles = %s''',
                    (vehicle_id, )
                    )
        location_id = cur.fetchone()[0]

        if not location_id:
            response['error'] = 'Unable to get Location ID for given Vehicle ID'
            return jsonify(response)

        cur.execute('''UPDATE LogisticCompany.Location
                    SET Latitude = %s, Longitude = %s
                    WHERE idLocation = %s''',
                    (latitude, longitude, location_id, ))

        mysql.connection.commit()

        # forward update to webapp
        send_vehicle_update_to_webapp(vehicle_id, latitude, longitude)

    except KeyError:
        response['error'] = 'Invalid JSON'

    return jsonify(response)


def send_vehicle_update_to_webapp(vehicle_id, latitude, longitude):
    url = 'http://10.90.138.37:8083/update_position'
    data = {'id': vehicle_id,
            'latitude': latitude,
            'longitude': longitude,
            }

    r = requests.post(url, json=data)
    if r.status_code != 200:
        pass
        # log it or something?

