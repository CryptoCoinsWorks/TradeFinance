import os
import ast
import json
import sqlite3
import hashlib, uuid, hmac
from utils import constants as cst
from cryptography.fernet import Fernet


##### DATABASE Functions #####


def connection_to_db(db_path):
    """This method create connection for Database
    """
    connection = sqlite3.connect(db_path)
    return connection


def create_user(db_connection, user, mail, password):
    """Create a new user into Database
    """
    req = """INSERT INTO users (user_username, mail, password) VALUES (?,?,?)"""
    cursor = db_connection.cursor()
    cursor.execute(req, (user, mail, password))
    db_connection.commit()
    return cursor.lastrowid


def create_position(db_connection, data):
    """Create a Data when a position is create.
    """
    user_id = get_user_id(db_connection, "admin")[0]
    req = """INSERT INTO positions (user_id, ticker, order_type, order_execution, amount,
                                    price, stop_price, limit_price, date, take_profit,
                                    stop_loss) VALUES (?,?,?,?,?,?,?,?,?,?,?)"""
    cursor = db_connection.cursor()
    cursor.execute(req, (user_id, data['ticker'], data['order_type'], data['order_execution'],
                         data['amount'], data['price'], data['stop'], data['limit'],
                         data['date'], data['take_profit'], data['stop_loss']))
    db_connection.commit()
    return cursor.lastrowid


def add_favorite(db_connection, ticker, name):
    """Add favorite for user
    """
    req_check = """SELECT * FROM favorites WHERE user_id=? AND ticker=? AND name=?"""
    req = """INSERT OR IGNORE INTO favorites (user_id, ticker, name) VALUES (?, ?, ?)"""
    cursor = db_connection.cursor()
    user_id = get_user_id(db_connection, "admin")[0]
    if not cursor.execute(req_check, (user_id, ticker, name)).fetchall():
        cursor.execute(req, (user_id, ticker, name))
        db_connection.commit()


def add_chart(db_connection, ticker, data):
    """Save chart data into Database.
        Create Data if not exist, else update it.
    """
    req = """SELECT * FROM charts WHERE user_id = ? AND ticker = ?"""
    cursor = db_connection.cursor()
    id = get_user_id(db_connection, "admin")[0]
    if not cursor.execute(req, (id, ticker)).fetchone():
        req = """INSERT INTO charts (user_id, data, ticker) VALUES (?, ?, ?)"""
        cursor.execute(req, [id, json.dumps(data), ticker])
    else:
        req = """UPDATE charts SET data=? WHERE user_id=? AND ticker=?"""
        cursor.execute(req, (json.dumps(data), id, ticker))
    db_connection.commit()
    return cursor.lastrowid


def get_user_id(db_connection, user_name):
    """Get Id from the database using user_name
    """
    req = """SELECT user_id FROM users WHERE user_username = ?"""
    cursor = db_connection.cursor()
    cursor.execute(req, (user_name,))
    return cursor.fetchone()


def get_all_users(db_connection):
    req = """SELECT * FROM users"""
    cursor = db_connection.cursor()
    cursor.execute(req)
    return cursor.fetchall()


def find_user_login(db_connection, user, password, type_field="user_username"):
    """This method is use to check if right data to login.
    """
    req = """SELECT * FROM users WHERE {}= ? AND password= ?""".format(type_field)
    cursor = db_connection.cursor()
    cursor.execute(req, (user, password))
    return cursor.fetchone()


def find_position_from_id(db_connection, id):
    """This method get user using user_id
        """
    req = """SELECT * FROM positions WHERE position_id=?"""
    cursor = db_connection.cursor()
    cursor.execute(req, (id,))
    return cursor.fetchone()


def get_user_by_id(db_connection, user_id):
    """This method get user using user_id
    """
    req = """SELECT * FROM users WHERE user_id=?"""
    cursor = db_connection.cursor()
    cursor.execute(req, (user_id,))
    return cursor.fetchone()


def get_chart_data(db_connection, ticker):
    """This method get data for a select chart.
    """
    req = """SELECT data FROM charts WHERE ticker = ?"""
    cursor = db_connection.cursor()
    if cursor.execute(req, (ticker,)).fetchone():
        cursor.execute(req, (ticker,))
        data_chart = cursor.fetchone()[0]
        return ast.literal_eval(data_chart)


def get_positions(db_connection):
    """Get all the position from a user
    """
    req = """SELECT * FROM positions WHERE user_id = ?"""
    cursor = db_connection.cursor()
    id = get_user_id(db_connection, "admin")[0]
    cursor.execute(req, (id,))
    return cursor.fetchall()


def get_position_by_id(db_connection, id):
    req = """SELECT * FROM positions WHERE user_id=? and position_id=?"""
    cursor = db_connection.cursor()
    user_id = get_user_id(db_connection, "admin")[0]
    cursor.execute(req, (user_id, id))
    return cursor.fetchone()


def update_position(db_connection, id, data):
    """Modify position from the database
    """
    req = """UPDATE positions SET ticker=?, order_type=?, order_execution=?, amount=?,
                                    price=?, stop_price=?, limit_price=?, date=?, take_profit=?,
                                    stop_loss=? WHERE user_id=? AND position_id=?"""
    cursor = db_connection.cursor()
    user_id = get_user_id(db_connection, "admin")[0]
    cursor.execute(req, (data[1], data[2], data[3], data[4], data[5], data[6],
                         data[7], data[8], data[9], data[10], user_id, id))
    db_connection.commit()


def close_position(db_connection, id):
    """ Delete position from the Database
    """
    req = """DELETE FROM positions WHERE user_id=? AND position_id=?"""
    cursor = db_connection.cursor()
    user_id = get_user_id(db_connection, "admin")[0]
    cursor.execute(req, (user_id, id))
    db_connection.commit()


def sanity_check_mail_exist(db_connection, mail):
    """This method check if email exist.
        To avoid having same email adress when new regiser.
    """
    req = """SELECT * FROM users WHERE mail = ?"""
    cursor = db_connection.cursor()
    cursor.execute(req, (mail,))
    data = cursor.fetchall()
    if not data:
        return True


def get_favorite_for_user(db_connection):
    """This get all favorites from a user_id
    """
    req = """SELECT * FROM favorites WHERE user_id=?"""
    cursor = db_connection.cursor()
    user_id = get_user_id(db_connection, "admin")[0]
    cursor.execute(req, (user_id,))
    data = cursor.fetchall()
    favorites = list()
    if data:
        for fav in data:
            favorites.append({"ticker": fav[1],
                              "name": fav[2]})
    return favorites


def remove_fav(db_connection, ticker, name):
    """ This remove favorites from its ticker/name
    """
    req = """DELETE FROM favorites WHERE user_id=? AND ticker=? AND name=?"""
    cursor = db_connection.cursor()
    user_id = get_user_id(db_connection, "admin")[0]
    cursor.execute(req, (user_id, ticker, name))
    db_connection.commit()


##### CRYPTOGRAPHY Functions #####


def crypt_password(password):
    """This method crypt password.
    """
    salt = cst.PRIVATE_KEY
    pw_hash = hashlib.pbkdf2_hmac('sha256',
                                  password.encode(),
                                  salt.encode(),
                                  100000)
    return pw_hash
