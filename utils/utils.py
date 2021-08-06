""" Utility functions for Akvelon task runner

Author: Slobodan Kostic
slobodan.kostic14@gmail.com
"""

import re
from utils.constants import DATE_FORMAT

def check_email_validity(email):
    """ Checks e-mail validity (i.e. if only one @ is found and at least one (sub)domain)

    :param email: email which is to be checked
    :type email: str
    :return: True, if email is valid, otherwise False
    """
    if email.count('@') != 1:
        return False
    if len(email.split('@')[0]) == 0:
        return False
    if '.' not in email.split('@')[1]:
        return False
    return True

def validate_user_request_dict(request_dict):
    """ Checks user request dictionary validity (i.e. whether the correct fields are provided)

    :param request_dict: Dictionary which is to be checked
    :type request_dict: dict
    :return: True, if request_dict is valid, otherwise False
    """
    if 'first_name' not in request_dict:
        return False
    if 'last_name' not in request_dict:
        return False
    if 'id' not in request_dict:
        return False
    if 'email' not in request_dict:
        return False
    return True

def validate_transaction_dict(request_dict):
    """ Checks transaction request dictionary validity (i.e. whether the correct fields are provided)

    :param request_dict: Dictionary which is to be checked
    :type request_dict: dict
    :return: True, if request_dict is valid, otherwise False
    """
    if 'id' not in request_dict:
        return False
    if 'user_id' not in request_dict:
        return False
    if 'amount' not in request_dict:
        return False
    if 'date' not in request_dict:
        return False
    return True

def validate_date_format(date):
    """ Checks the date format validity (i.e. YYYY-MM-DD)

    :param date: Date, whose format is to be checked
    :type date: str
    :return: True, if date format is valid, otherwise False
    """
    return re.match(DATE_FORMAT, date)

def fibonacci(num):
    """ Fibonacci calculator, based on the provided number.
    Throws a TypeError exception if integer is not provided.

    :param num: Number for which the Fibonacci sum is calculated.
    :type num: int
    :return: Fibonacci(n) if n is correct, otherwise 0
    """
    if not isinstance(num, int):
        raise TypeError('Fibonacci function requires an integer parameter')
    if num < 1:
        return 0
    if num == 1:
        return 1
    sum = 0
    a, b = 0, 1

    for _ in range(num - 1):
        sum = a + b
        a = b
        b = sum
    return sum
