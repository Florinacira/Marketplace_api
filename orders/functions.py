import pprint

from database.functions import read_database, write_database
from uuid import uuid4
from datetime import datetime
from flask import Response


def create_order():
    print('Creating a order...')
    data = read_database()
    print(data)
    order_id = str(uuid4())
    user_id, product_id = None, None
    user_email = input('Input your email: ')
    for userid, user in data['users'].items():
        if user['email'] == user_email:
            user_id = userid
            break

    order = input('Input the product you want to order: ')
    for productid, product in data['products'].items():
        if product['product_name'] == order:
            product_id = productid
            break
    else:
        print('The product is not in stock')

    if user_id is not None and product_id is not None:

        register_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        data['orders'][order_id] = {
            'user_id': user_id,
            'product_id': product_id,
            'register_date': register_date
            }

        write_database(data)
        print('Done creating order...')
    else:
        print('Invalid user or product')


def delete_order():
    data = read_database()
    order_to_id = {}
    for order_id, order in data['orders'].items():
        for product_id, product in data['products'].items():
            order_to_id[product['product_name']] = order_id

    product_of_order_to_remove = input(f"Please input the product of order you want to remove: ")
    order_to_remove = order_to_id.get(product_of_order_to_remove)
    if order_to_remove in data['orders']:
        del data['orders'][order_to_remove]
        write_database(data)
        print(data)


def list_orders():
    data = read_database()
    orders = data.get('orders')
    if orders:
        pprint.pprint(orders)
    else:
        print('No orders in DB')


def list_order():
    data = read_database()
    orders = data.get('orders')

    for order_id, order in orders.items():
        pprint.pprint(order_id)
    input_order_id = input('Please input id of order you want to display: ')
    for order_id, order in orders.items():
        if order_id == input_order_id:
            pprint.pprint(order)
            break
    else:
        print(f"No order with id {input_order_id} has been found in DB!")


def update_order():
    data = read_database()
    orders = data.get('orders')
    for order_id, order in orders.items():
        pprint.pprint(order_id)

    input_order = input('Please input id of order you want to update:')
    updated_product_of_order = input('Please input updated product id of the order: ')
    for order_id, order in orders.items():
        if order_id == input_order:
            order['product_id'] = updated_product_of_order if updated_product_of_order else order['product_id']
            break
    else:
        print(f'No order with id {input_order} has been found!')

    write_database(data)


## WEB APIs


def add_order_flask(email, product_name):
    data = read_database()
    orders = data.get('orders')
    order_id = str(uuid4())
    register_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    user_id, product_id = None, None

    for userid, user in data['users'].items():
        if user['email'] == email:
            user_id = userid
            break

    for productid, product in data['products'].items():
        if product['product_name'] == product_name:
            product_id = productid
            break
    else:
        print('The product is not in stock')

    if user_id is not None and product_id is not None:

        orders[order_id] = {
            'user_id': user_id,
            'product_id': product_id,
            'register_date': register_date
        }
        write_database(data)
        return 201, f"Order with id = {order_id} has been created"
    else:
        print('Invalid user or product')


def delete_order_flask(order_id):
    data = read_database()
    orders = data.get('orders')
    if order_id in orders:
        del orders[order_id]
        write_database(data)
        return Response(status=200, response=f'Order with id:{order_id} has been deleted')
    else:
        return Response(status=404, response=f'Order with id:{order_id} not found')


def get_order_flask(order_id):
    data = read_database()
    orders = data.get('orders', {})
    if order_id in orders:
        return 200, orders[order_id]
    else:
        return 404, f'Order with id {order_id} not found'


def list_orders_flask():
    data = read_database()
    orders = data.get('orders')
    if orders:
        return 200, orders
    else:
        return 400, 'No orders in DB'


def update_order_flask(order_id, order_data):
    data = read_database()
    orders = data.get('orders')
    if order_id in orders:
        data['orders'][order_id].update(order_data)
        write_database(data)
        return 200, f'Order with id: {order_id} has been successfully updated'
    else:
        return 404, f'Order with id: {order_id} not found'







