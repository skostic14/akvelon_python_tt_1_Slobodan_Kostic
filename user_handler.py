""" Transaction handler for Akvelon task runner

Handles all database operations (CRUD) related to transactions.

Author: Slobodan Kostic
slobodan.kostic14@gmail.com
"""

from flask import g

def create_user_list_from_sqlite_rows(rows):
    """ Creates a list of users based on the extracted SQLite rows

    :param rows: list of tuples with the order (user_id, first name, last name, email)
    :type rows: list(tuple)
    :returns: a list of users
    """
    users = []
    for row in rows:
        user_id = row[0]
        first_name = row[1]
        last_name = row[2]
        email = row[3]
        users.append({
            'id': user_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        })
    return users

def insert_user(user):
    """ Inserts a new user entry in the database.

    :param user: User to be inserted
    :type user: User
    """
    cursor = g.db.cursor()
    cursor.execute('INSERT INTO users '
                    '(id, first_name, last_name, email) '
                    'VALUES (%d, \"%s\", \"%s\", \"%s\");'
                    % (user.id, user.first_name, user.last_name, user.email))
    g.db.commit()
    cursor.close()

def find_users_by_uid(user_id):
    """ Finds user(s) by the user ID.

    :param user_id: User ID
    :type user_id: int
    :returns: A list of found users
    """
    cursor = g.db.cursor()
    cursor.execute('SELECT * FROM users '
                    'WHERE id=%d' % user_id)
    users = create_user_list_from_sqlite_rows(cursor)
    cursor.close()
    return users

def find_users_by_first_name(first_name):
    """ Finds user(s) by the first name.

    :param first_name: First name
    :type first_name: str
    :returns: A list of found users
    """
    cursor = g.db.cursor()
    cursor.execute('SELECT * FROM users '
                    'WHERE first_name=\"%s\"' % first_name)
    users = create_user_list_from_sqlite_rows(cursor)
    cursor.close()
    return users

def find_users_by_last_name(last_name):
    """ Finds user(s) by the last name.

    :param last_name: Last name
    :type last_name: str
    :returns: A list of found users
    """
    cursor = g.db.cursor()
    cursor.execute('SELECT * FROM users '
                    'WHERE last_name=\"%s\"' % last_name)
    users = create_user_list_from_sqlite_rows(cursor)
    cursor.close()
    return users

def find_users_by_email(email):
    """ Finds user(s) by the e-mail.

    :param email: e-mail
    :type email: str
    :returns: A list of found users
    """
    cursor = g.db.cursor()
    cursor.execute('SELECT * FROM users '
                    'WHERE email=\"%s\"' % email)
    users = create_user_list_from_sqlite_rows(cursor)
    cursor.close()
    return users

def find_all_users():
    """ Gets all users from the database.

    :returns: A list of all users
    """
    cursor = g.db.cursor()
    cursor.execute('SELECT * FROM users')
    users = create_user_list_from_sqlite_rows(cursor)
    cursor.close()
    return users

def modify_user(user):
    """ Modifies a user in the database based on their ID.

    :param user: User which is to be modified based on the ID.
    :type user: User
    """
    cursor = g.db.cursor()
    cursor.execute('UPDATE users SET first_name=\"%s\", last_name=\"%s\", email=\"%s\" WHERE id=%d'
                    % (user.first_name, user.last_name, user.email, user.id))
    g.db.commit()
    cursor.close()

def delete_user(user_id):
    """ Deletes a user from the database based on their ID.

    :param user_id: ID of the user which is to be deleted.
    :type user_id: int
    """
    cursor = g.db.cursor()
    cursor.execute('DELETE FROM users WHERE id=%d' % user_id)
    g.db.commit()
    cursor.close()
