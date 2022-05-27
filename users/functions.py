import pprint
from datetime import datetime
from uuid import uuid4

from database.functions import read_database, write_database
from flask import Response


def is_valid_email(email):
    """Returns whether an email address string is valid or not.
        :param email: email address str
        :return: tuple of form (True/False, message) if valid/not valid with message explaining the error
    """
    special_characters = "!#$%^&*()|\\{}[]'\":;/><,`~"

    if email.count('@') != 1:
        return False, "Email address should contain exactly one @ symbol!"
    if email.count('.') < 1:
        return False, "Email address should contain at least one . symbol!"
    if email.lower() != email:
        return False, "Email address should contain only lowercase letters!"
    if any(c in email for c in special_characters):
        return False, f"Email address should not contain any of the following special_characters: {special_characters}"
    return True, ''


def create_user():

    print('Creating a user...')
    data = read_database()
    print(data)

    user_id = str(uuid4())
    name = input('Input your user name: ')
    email = input('Input your user email: ')
    while True:
        validation, message = is_valid_email(email)
        if validation == True:
            break
        else:
            print(message)
            email = input('Please input a valid email adress: ')

    register_date = datetime.now().strftime('%Y-%m-%d %H:%M')

    data['users'][user_id] = {
        "name": name,
        "email": email,
        "register_date": register_date
    }
    write_database(data)
    print('Done creating user!')


def delete_user():
    data = read_database()
    user_name_to_id = {}
    for user_id, user in data['users'].items():
        user_name_to_id[user['name']] = user_id
    print(data)
    name_to_remove = input(f"Please input the name you want to remove from: {user_name_to_id}!\n")
    id_to_remove = user_name_to_id.get(name_to_remove)
    if id_to_remove in data['users']:
        del data['users'][id_to_remove]
        write_database(data)
        print(data)


def list_user():
    data = read_database()
    users = data.get('users')

    input_email = input('Please input email of users you want to display: ')

    for user_id, user in users.items():
        if user['email'] == input_email:
            pprint.pprint(user)
            break
    else:
        print(f"No user with email {input_email} has been found in DB!")


def list_users():
    data = read_database()
    users = data.get('users')
    if users:
        pprint.pprint(users)
        # print(json.dumps(users, indent=4))
    else:
        print('No userS in DB!')


def update_user():
    data = read_database()
    users = data.get('users')

    input_email = input('Please input email of user you want to update:  ')
    updated_email = input('Please input updated email: ')
    updated_name = input('Please input update name: ')

    for user_id, user in users.items():
        if user['email'] == input_email:
            user['name'] = updated_name if updated_name else user['name']
            user['email'] = updated_email if updated_email else user['email']
            break
    else:
        print(f'No user with email {input_email} has been found!')

    write_database(data)


## WEB APIs


def create_user_flask(name, email):
    data = read_database()
    if not is_valid_email(email):
        return 400, 'Validation error...'
    
    users = data.get('users')
    user_id = str(uuid4())
    register_date = datetime.now().strftime('%Y-%m-%d %H:%M')

    users[user_id] = {
        'name': name,
        'email': email,
        'register_date': register_date
    }
    write_database(data)
    return 201, f"User with id = {user_id} has been created"


def delete_user_flask(user_id):
    data = read_database()
    users = data.get('users')

    if user_id in users:
        del users[user_id]
        write_database(data)
        return Response(status=200, response=f'user with id{user_id} has been deleted')
    else:
        return Response(status=404, response=f'user with id{user_id} not found')


def get_user_flask(user_id):
    data = read_database()
    users = data.get('users', {})
    if user_id in users:
        return 200, users[user_id]
    else:
        return 404, f'User with id {user_id} not found'


def list_users_flask():
    data = read_database()
    users = data.get('users')
    if users:
        return 200, users
    else:
        return 400, 'No users in DB'


def update_user_flask(user_id, user_data):
    data = read_database()
    users = data.get('users')
    if user_id in users:
        data['users'][user_id].update(user_data)
        write_database(data)
        return 200, f'user with id: {user_id} has been successfully updated'
    else:
        return 404, f'user with id: {user_id} not found'








