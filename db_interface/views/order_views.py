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


@app.route('/add_order', methods=['POST', ])
def add_order():
    """
    response = {'error': 'not implemented'}
    return jsonify(response)

    """
    response = {'error': 'none'}
    if not request.is_json:
        response['error'] = 'JSON expected'
        return jsonify(response)

    try:
        j = request.get_json()
        cur = mysql.connection.cursor()
        args = [0]

        # select delivery types to check them
        cur.execute("SELECT Type from LogisticCompany.DeliveryType")
        delivery_types = cur.fetchall()
        delivery_types = [dt[0] for dt in delivery_types]

        if j['delivery_type'] not in delivery_types:
            response['error'] = 'Invalid delivery type'
            return jsonify(response)

        # check if pickup type is correct
        cur.execute("SELECT Type from LogisticCompany.PickUpType")
        pickup_types = cur.fetchall()
        pickup_types = [pt[0] for pt in pickup_types]

        if j['pickup_type'] not in pickup_types:
            response['error'] = 'Invalid pickup type'
            return jsonify(response)

        db_proc = 'logged_in'

        if 'customer_id' in j:
            args.append(j['customer_id'])
        else:
            db_proc = 'logged_out'

        if 'id' in j['sender']:
            if db_proc == 'logged_out':
                response['error'] = 'Can\'t use id\'s without customer id, sorry'
                return jsonify(response)

            else:
                db_proc = 'with_contact'

            args.append(j['sender']['id'])

        else:
            args += [j['sender']['name'], j['sender']['surname'],
                            j['sender']['phone_number']]

        if 'id' in j['sender']['address']:
            if db_proc == 'logged_out':
                response['error'] = 'Can\'t use id\'s without customer id, sorry'
                return jsonify(response)

            elif db_proc == 'with_contact':
                db_proc = 'with_contact_and_address'

            else:
                db_proc = 'with_address'

            args.append(j['sender']['address']['id'])

        else:
            args += [
                    j['sender']['address']['country'],
                    j['sender']['address']['region'],
                    j['sender']['address']['city'],
                    j['sender']['address']['street'],
                    j['sender']['address']['building'],
                    j['sender']['address']['additional_info']
                ]

        args += [
                j['receiver']['name'], j['receiver']['surname'],
                j['receiver']['phone_number'],
                j['receiver']['address']['country'],
                j['receiver']['address']['region'],
                j['receiver']['address']['city'],
                j['receiver']['address']['street'],
                j['receiver']['address']['building'],
                j['receiver']['address']['additional_info'],

                j['attached_notes'],
                j['delivery_type'],
                j['pickup_type']
            ]

        cur = mysql.connection.cursor()

        if db_proc == 'logged_in':
            cur.callproc('LogisticCompany.AddOrderLoggedIn', args)
            cur.execute('SELECT @_LogisticCompany.AddOrderLoggedIn_0')
        elif db_proc == 'logged_out':
            cur.callproc('LogisticCompany.AddOrderLoggedOut', args)
            cur.execute('SELECT @_LogisticCompany.AddOrderLoggedOut_0')
        elif db_proc == 'with_address':
            cur.callproc('LogisticCompany.AddOrderWithAddress', args)
            cur.execute('SELECT @_LogisticCompany.AddOrderWithAddress_0')
        elif db_proc == 'with_contact':
            cur.callproc('LogisticCompany.AddOrderWithContact', args)
            cur.execute('SELECT @_LogisticCompany.AddOrderWithContact_0')
        elif db_proc == 'with_contact_and_address':
            # throw out customer_id as we don't need it
            del args[1]
            cur.callproc('LogisticCompany.AddOrderWithContactAndAddress', args)
            cur.execute('SELECT @_LogisticCompany.AddOrderWithContactAndAddress_0')

        res = cur.fetchone()
        response['order_id'] = res

        mysql.connection.commit()

    except KeyError:
        response['error'] = 'Invalid JSON'
    return jsonify(response)
