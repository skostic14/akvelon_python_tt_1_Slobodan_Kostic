""" User class for Akvelon task runner

Author: Slobodan Kostic
slobodan.kostic14@gmail.com
"""

class User():
    """ Data class used to describe a transaction.
    """
    def __init__(self, user_dict):
        self.id = user_dict['id']
        self.first_name = user_dict['first_name']
        self.last_name = user_dict['last_name']
        self.email = user_dict['email']
