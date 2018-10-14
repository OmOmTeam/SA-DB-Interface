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


@app.route('/orders_to_approve', methods=['GET', ])
def orders_to_approve():

    response = {'error': 'none', 'orders': []}
    cur = mysql.connection.cursor()

    cur.execute('CALL LogisticCompany.GetOrdersOnValidating')

    res = cur.fetchall()

    for order in res:
        order_id, sender_name, sender_surname, sender_telephone, \
                sender_country, sender_region, sender_city, sender_street, \
                sender_building_num, sender_addition_info, \
                receiver_name, receiver_surname, receiver_telephone, \
                receiver_country, receiver_region, receiver_city, \
                receiver_street, receiver_building_num, \
                receiver_addition_info, \
                attached_notes, status, delivery_type, pickup_type = order
        response['orders'].append({
                    'id': order_id,
                    'order_status': status,
                    'sender': {
                        'name': sender_name,
                        'surname': sender_surname,
                        'phone_number': sender_telephone,
                        'address': {
                            'country': sender_country,
                            'region': sender_region,
                            'city': sender_city,
                            'street': sender_street,
                            'building': sender_building_num,
                            'additional_info': sender_addition_info
                        }
                    },
                    'pickup_type': pickup_type,
                    'receiver': {
                        'name': receiver_name,
                        'surname': receiver_surname,
                        'phone_number': receiver_telephone,
                        'address': {
                            'country': receiver_country,
                            'region': receiver_region,
                            'city': receiver_city,
                            'street': receiver_street,
                            'building': receiver_building_num,
                            'additional_info': receiver_addition_info
                        }
                    },
                    'delivery_type': delivery_type,
                    'attached_notes': attached_notes
                })

    return jsonify(response)
