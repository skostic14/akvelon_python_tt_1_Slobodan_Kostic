""" Transaction class for Akvelon task runner

Author: Slobodan Kostic
slobodan.kostic14@gmail.com
"""

class Transaction():
    """ Data class used to describe a transaction.
    """
    def __init__(self, trans_dict):
        self.id = trans_dict['id']
        self.user_id = trans_dict['user_id']
        self.amount = trans_dict['amount']
        self.date = trans_dict['date']
