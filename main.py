""" Main module for Akvelon task runner

Handles all requests and uses respective handlers to read/write from the database.

Author: Slobodan Kostic
slobodan.kostic14@gmail.com
"""

import json
import sqlite3

from flask import Flask, request, g
from flask_swagger_ui import get_swaggerui_blueprint

from constants import DATABASE_FILENAME
from transaction import Transaction
import transaction_handler
from user import User
import user_handler
from utils import check_email_validity, validate_user_request_dict, validate_transaction_dict, validate_date_format


app = Flask(__name__)
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Akvelon task - Slobodan Kostic'
    }
)
app.register_blueprint(swaggerui_blueprint)

@app.before_request
def before_request():
    """ Connect to the SQLite database if it is not done before
    """
    if getattr(g, 'db', None) is None:
        g.db = sqlite3.connect(DATABASE_FILENAME)

@app.route('/create_user', methods=['POST'])
def create_user():
    """ Creates a new user in the users database
    """
    request_dict = request.get_json()
    if not validate_user_request_dict(request_dict):
        return 'Missing parameters', 400
    if not check_email_validity(request_dict['email']):
        return 'Invalid e-mail provided', 400
    user = User(request_dict)
    user_handler.insert_user(user)
    return 'User inserted successfully', 200

@app.route('/modify_user', methods=['POST'])
def modify_user():
    """ Modifies a user in the users database
    """
    request_dict = request.get_json()
    if not validate_user_request_dict(request_dict):
        return 'Missing parameters', 400
    if not check_email_validity(request_dict['email']):
        return 'Invalid e-mail provided', 400
    user = User(request_dict)
    user_handler.modify_user(user)
    return 'User modified successfully', 200

@app.route('/get_users', methods=['GET'])
def get_users():
    """ Gets a list of users depending on the given filters
    """
    user_id = request.args.get('user_id')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')

    if user_id is not None:
        users = user_handler.find_users_by_uid(user_id)
    elif first_name is not None:
        users = user_handler.find_users_by_first_name(first_name)
    elif last_name is not None:
        users = user_handler.find_users_by_last_name(last_name)
    elif email is not None:
        users = user_handler.find_users_by_email(email)
    else:
        users = user_handler.find_all_users()

    if not users:
        return 'No users have been found', 500
    return json.dumps({'users': users}), 200, {'ContentType': 'application/json'}

@app.route('/delete_user', methods=['GET'])
def delete_user():
    """ Deletes a user from the users database, based on the user ID
    """
    user_id = request.args.get('user_id')
    if user_id is None:
        return 'Missing user_id parameter', 400
    user_handler.delete_user(user_id)
    return 'User deleted successfully', 200

@app.route('/create_transaction', methods=['POST'])
def create_transaction():
    """Creates a new transaction in the transactions database.
    Requires a correct user ID before writing a transaction.
    """
    request_dict = request.get_json()
    if not validate_transaction_dict(request_dict):
        return 'Missing parameters', 400
    if not user_handler.find_users_by_uid(request_dict['user_id']):
        return 'Unknown user', 400
    transaction = Transaction(request_dict)
    transaction_handler.insert_transaction(transaction)
    return 'Transaction inserted successfully', 200

@app.route('/modify_transaction', methods=['POST'])
def modify_transaction():
    """Modifies a transaction in the transactions database.
    Requires a correct user ID before writing a transaction.
    """
    request_dict = request.get_json()
    if not validate_transaction_dict(request_dict):
        return 'Missing parameters', 400
    if not user_handler.find_users_by_uid(request_dict['user_id']):
        return 'Unknown user', 400
    transaction = Transaction(request_dict)
    transaction_handler.modify_transaction(transaction)
    return 'Transaction modified successfully', 200

@app.route('/get_transactions', methods=['GET'])
def get_transactions():
    """ Gets a list of transactions depending on the given filters
    """
    transaction_id = request.args.get('id')
    user_id = request.args.get('user_id')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    sort = request.args.get('sort')

    for date in [date_from, date_to]:
        if date is None:
            continue
        if not validate_date_format(date):
            return 'Invalid date format (YYYY-MM-DD)', 400

    if transaction_id is not None:
        transactions = transaction_handler.find_transactions_by_id(transaction_id)
    elif user_id is not None:
        transactions = transaction_handler.find_transactions_by_user_id(user_id)
    elif date_from is not None or date_to is not None:
        transactions = transaction_handler.get_all_transactions_by_date(start_date=date_from, end_date=date_to)
    else:
        transactions = transaction_handler.get_all_transactions()

    if sort == 'date':
        transactions.sort(key=lambda x: x['date'])
    elif sort == 'amount':
        transactions.sort(key=lambda x: x['amount'])
    return json.dumps({'transactions': transactions}), 200, {'ContentType': 'application/json'}

@app.route('/delete_transaction', methods=['GET'])
def delete_transaction():
    """ Deletes a transaction from the database, based on the user ID
    """
    transaction_id = request.args.get('id')
    if transaction_id is None:
        return 'Missing id parameter', 400
    transaction_handler.delete_transaction(int(transaction_id))
    return 'Transaction deleted successfully', 200

# Uncomment the block below to use the module in debug environment
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
"""
