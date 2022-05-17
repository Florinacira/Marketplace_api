import json
from users.functions import *
from flask import Flask, request, Response
from products.functions import *
from orders.functions import *
app = Flask('Marketplace API')

#users


@app.route('/create_user', methods=['POST'])
def create_user():
    post_data = json.loads(request.data)
    name = post_data['name']
    email = post_data["email"]
    status_code, user_returned = create_user_flask(name, email)
    return Response(status=status_code, response=json.dumps(user_returned))


@app.route('/delete_user/<user_id>', methods=["DELETE"])
def delete_user(user_id):
    return delete_user_flask(user_id)


@app.route('/get_user/<user_id>', methods=['GET'])
def get_user(user_id):
    status_code, users_returned = get_user_flask(user_id)
    return Response(status=status_code, response=json.dumps(users_returned))


@app.route('/list_users', methods=['GET'])
def list_users():
    status_code, users_returned = list_users_flask()
    return Response(status=status_code, response=json.dumps(users_returned))


@app.route('/update_user/<user_id>', methods=['PATCH'])
def update_user(user_id):
    user_data = json.loads(request.data)
    status_code, message = update_user_flask(user_id, user_data)
    return Response(status=status_code, response=message)


#products

@app.route('/create_product', methods=['POST'])
def create_product():
    post_data = json.loads(request.data)
    product_name = post_data['product_name']
    category = post_data['category']
    price = post_data['price']
    status_code, product_returned = create_product_flask(product_name, category, price)
    return Response(status=status_code, response=json.dumps(product_returned))


@app.route('/delete_product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    return delete_product_flask(product_id)


@app.route('/get_product/<product_id>', methods=['GET'])
def get_product(product_id):
    status_code, products_returned = get_product_flask(product_id)
    return Response(status=status_code, response=json.dumps(products_returned))


@app.route('/list_products', methods=['GET'])
def list_products():
    status_code, products_returned = list_products_flask()
    return Response(status=status_code, response=json.dumps(products_returned))


@app.route('/update_product/<product_id>', methods=['PATCH'])
def update_product(product_id):
    product_data = json.loads(request.data)
    status_code, message = update_product_flask(product_id, product_data)
    return Response(status=status_code, response=message)

#orders


@app.route('/add_order', methods=['POST'])
def add_order():
    post_data = json.loads(request.data)
    email = post_data['email']
    product_name = post_data['product_name']
    status_code, order_returned = add_order_flask(email, product_name)
    return Response(status=status_code, response=json.dumps(order_returned))


@app.route('/delete_order/<order_id>', methods=["DELETE"])
def delete_order(order_id):
    return delete_order_flask(order_id)


@app.route('/get_order/<order_id>', methods=['GET'])
def get_order(order_id):
    status_code, order_returned = get_order_flask(order_id)
    return Response(status=status_code, response=json.dumps(order_returned))


@app.route('/list_orders', methods=['GET'])
def list_orders():
    status_code, orders_returned = list_orders_flask()
    return Response(status=status_code, response=json.dumps(orders_returned))


@app.route('/update_order/<order_id>', methods=['PATCH'])
def update_order(order_id):
    order_data = json.loads(request.data)
    status_code, message = update_order_flask(order_id, order_data)
    return Response(status=status_code, response=message)


if __name__ == '__main__':
    app.run()