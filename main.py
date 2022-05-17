from users.functions import *
from products.functions import *
from orders.functions import *

def print_menu_options():
    print(f'Available options: {list(menu_options.keys())} ')

def exit_message():
    print('Have a nice day!')

menu_options = {
    'create_user': create_user,
    'delete_user': delete_user,
    'list_user': list_user,
    'list_users': list_users,
    'update_user': update_user,
    'create_product': create_product,
    'delete_product': delete_product,
    'list_products': list_products,
    'list_product': list_product,
    'update_product': update_product,
    'create_order': create_order,
    'delete_order': delete_order,
    'list_orders': list_orders,
    'list_order': list_order,
    'update_order': update_order,
    'help': print_menu_options,
    'exit': exit_message
}

def main():
    option = ''
    while option != "exit":
        option = input("Choose an option (type help for menu options): ")
        function_to_call = menu_options.get(option)
        if function_to_call:
            function_to_call()
        else:
            print("You did not input a valid option")
            print_menu_options()

if __name__ == '__main__':
    main()