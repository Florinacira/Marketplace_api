from database.functions import read_database, write_database
from uuid import uuid4
import pprint
from flask import Response

def create_product():
    print('Creating a product...')
    data = read_database()
    print(data)

    product_id = str(uuid4())
    product_name = input('Input the product name: ')
    category = input('Input the category of the product: ')
    price = input('Input the price: ')

    data['products'][product_id]= {
        "product_name": product_name,
        "category": category,
        "price": price
    }
    write_database(data)
    print('Done creating the product!')


def delete_product():
    data = read_database()
    product_name_to_id = {}
    for product_id, product in data['products'].items():
        product_name_to_id[product['product_name']] = product_id
    print(data)
    product_to_remove = input(f'Please input the product you want to remove from {product_name_to_id}: \n')
    id_to_remove = product_name_to_id.get(product_to_remove)
    if id_to_remove in data['products']:
        del data['products'][id_to_remove]
        write_database(data)
        print(data)


def list_products():
    data = read_database()
    products = data.get('products')
    if products:
        pprint.pprint(products)
    else:
        print('No products in DB!')


def list_product():
   data = read_database()
   products = data.get('products')

   input_product = input('Please input the product you want to display: ')

   for product_id, product in products.items():
       if product['product_name'] == input_product:
           pprint.pprint(product)
           break
   else:
        print(f'No product with name {input_product} has been found in DB!')


def update_product():
    data = read_database()
    products = data.get('products')

    input_product = input('Please input the product to update: ')
    update_name_of_product = input('Input updated product:')
    update_category = input('Input updated category:')
    updated_price = input('Input updated price:')

    for product_id, product in products.items():
        if product['product_name'] == input_product:
            product['product_name'] = update_name_of_product if update_name_of_product else product['product_name']
            product['category'] = update_category if update_category else product['category']
            product['price'] = updated_price if updated_price else product['price']
            break
    else:
        print(f'No product with name {input_product} has been found!')

    write_database(data)

## WEB APIs

def create_product_flask(product_name, category, price):
    data = read_database()
    products = data.get('products')
    product_id = str(uuid4())

    products[product_id] = {
        'product_name': product_name,
        'category': category,
        'price': price
    }
    write_database(data)
    return 201, f"Product with id = {product_id} has been created!"

def delete_product_flask(product_id):
    data = read_database()
    products = data.get('products')

    if product_id in products:
        del products[product_id]
        write_database(data)
        return Response(status=200, response=f'product with id{product_id} has been deleted')
    else:
        return Response(status=404, response=f'Product with id{product_id} not found')

def get_product_flask(product_id):
    data = read_database()
    products = data.get('products', {})
    if product_id in products:
        return 200, products[product_id]
    else:
        return 404, f'Product with id {product_id} not found'

def list_products_flask():
    data = read_database()
    products = data.get('products')
    if products:
        return 200, products
    else:
        return 400, 'No products in DB'

def update_product_flask(product_id, product_data):
    data = read_database()
    products = data.get('products')
    if product_id in products:
        data['products'][product_id].update(product_data)
        write_database(data)
        return 200, f'Product with id: {product_id} has been successfully updated'
    else:
        return 404, f'Product with id: {product_id} not found'

