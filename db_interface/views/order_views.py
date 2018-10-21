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


@app.route('/orders', methods=['GET', ])
def get_orders():
    response = {'error': 'none', 'orders': []}
    cur = mysql.connection.cursor()

    cur.execute('CALL LogisticCompany.GetOrders')

    res = cur.fetchall()
    response['orders'] = unfold_orders(res)

    return jsonify(response)


@app.route('/get_order_by_id', methods=['GET', ])
def get_order_by_id():
    response = {'error': 'none', 'orders': []}

    if not request.is_json:
        response['error'] = 'JSON expected'
        return jsonify(response)

    else:
        cur = mysql.connection.cursor()

        try:
            order_id = request.get_json['order_id']

        except KeyError:
            response['error'] = 'Invalid JSON'
            return jsonify(response)

        cur.execute('CALL LogisticCompany.GetOrders')

        res = cur.fetchall()
        response['orders'] = next((item for item in unfold_orders(res) if item['id'] == order_id), None)

    return jsonify(response)


@app.route('/orders_to_approve', methods=['GET', ])
def orders_to_approve():

    response = {'error': 'none', 'orders': []}
    cur = mysql.connection.cursor()

    cur.execute('CALL LogisticCompany.GetOrdersOnValidating')

    res = cur.fetchall()
    response['orders'] = unfold_orders(res)

    return jsonify(response)


def unfold_orders(query_results):
    """
    Since at least 3 queries return orders in following format,
    I thinks it's a good idea to have one function
    for unfolding similar query results into dictionary
    """
    orders = []

    for order in query_results:
        order_id, sender_name, sender_surname, sender_telephone, \
                sender_country, sender_region, sender_city, sender_street, \
                sender_building_num, sender_addition_info, \
                receiver_name, receiver_surname, receiver_telephone, \
                receiver_country, receiver_region, receiver_city, \
                receiver_street, receiver_building_num, \
                receiver_addition_info, \
                attached_notes, status, delivery_type, pickup_type = order
        orders.append({
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

        return orders
