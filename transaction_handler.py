""" Transaction handler for Akvelon task runner

Handles all database operations (CRUD) related to transactions.

Author: Slobodan Kostic
slobodan.kostic14@gmail.com
"""

from flask import g

def create_transactions_list_from_sqlite_rows(rows):
    """ Creates a list of transactions based on the extracted SQLite rows

    :param rows: list of tuples with the order (trans_id, user_id, amount, date)
    :type rows: list(tuple)
    :returns: a list of transactions
    """
    transactions = []
    for row in rows:
        transaction_id = row[0]
        user_id = row[1]
        amount = row[2]
        date = row[3]
        transactions.append({
            'id': transaction_id,
            'user_id': user_id,
            'amount': amount,
            'date': date
        })
    return transactions

def insert_transaction(transaction):
    """ Inserts a new Transaction entry in the database.

    :param transaction: Transaction to be inserted
    :type transaction: Transaction
    """
    cursor = g.db.cursor()
    cursor.execute('INSERT INTO transactions '
                   '(id, user_id, amount, date) '
                   'VALUES (%d, %d, %f, datetime(\"%s\"))'
                   % (transaction.id, transaction.user_id, transaction.amount, transaction.date))
    g.db.commit()
    cursor.close()

def find_transactions_by_id(trans_id):
    """ Finds transaction(s) by the transaction ID.

    :param trans_id: Transaction ID
    :type trans_id: int
    :returns: A list of found transactions
    """
    cursor = g.db.cursor()
    cursor.execute('SELECT * FROM transactions WHERE id=%d' % trans_id)
    transactions = create_transactions_list_from_sqlite_rows(cursor)
    cursor.close()
    return transactions

def find_transactions_by_user_id(user_id):
    """ Finds transaction(s) by the user ID.

    :param user_id: User ID
    :type user_id: int
    :returns: A list of found transactions
    """
    cursor = g.db.cursor()
    cursor.execute('SELECT * FROM transactions WHERE user_id=%d' % user_id)
    transactions = create_transactions_list_from_sqlite_rows(cursor)
    cursor.close()
    return transactions

def get_all_transactions_by_date(start_date=None, end_date=None):
    """ Finds transaction(s) by the start and end date. If neither are provided, finds all transactions.

    :param start_date: Date defined as YYYY-MM-DD
    :type start_date: string
    :param end_date: Date defined as YYYY-MM-DD
    :type end_date: string
    :returns: A list of found transactions, grouped day-by-day
    """
    cursor = g.db.cursor()
    if start_date is not None and end_date is not None:
        cursor.execute('SELECT amount, date FROM transactions '
                       'WHERE date BETWEEN datetime(\"%s\") AND datetime(\"%s\")'
                       % (start_date, end_date))
    elif start_date is not None and end_date is None:
        cursor.execute('SELECT amount, date FROM transactions '
                       'WHERE date >= datetime(\"%s\")' % start_date)
    elif start_date is None and end_date is not None:
        cursor.execute('SELECT amount, date FROM transactions '
                       'WHERE date <= datetime(\"%s\")' % end_date)
    else:
        cursor.execute('SELECT amount, data FROM transactions')
    transactions = []
    day_by_day = {}
    for transaction in cursor:
        date = transaction[1].split(" ")[0]
        if date not in day_by_day:
            day_by_day[date] = 0.0
        day_by_day[date] += transaction[0]
    for date, amount in day_by_day.items():
        transactions.append({
            'date': date,
            'amount': amount
        })
    cursor.close()
    return transactions

def get_all_transactions():
    """ Gets all transactions from the database.

    :returns: A list of all transactions.
    """
    cursor = g.db.cursor()
    cursor.execute('SELECT * FROM transactions')
    transactions = create_transactions_list_from_sqlite_rows(cursor)
    cursor.close()
    return transactions

def modify_transaction(transaction):
    """ Modifies a transaction in the database based on its ID.

    :param transaction: Transaction which is to be modified based on the ID.
    :type transaction: Transaction
    """
    cursor = g.db.cursor()
    cursor.execute('UPDATE transactions SET user_id=%d, date=datetime(\"%s\"), amount=%f WHERE id=%d'
                    % (transaction.user_id, transaction.date, transaction.amount, transaction.id))
    g.db.commit()
    cursor.close()

def delete_transaction(transaction_id):
    """ Deletes a transaction from the database based on its ID.

    :param transaction_id: ID of the Transaction which is to be deleted
    :type transaction_id: int
    """
    cursor = g.db.cursor()
    cursor.execute('DELETE FROM transactions WHERE id=%d' % transaction_id)
    g.db.commit()
    cursor.close()
