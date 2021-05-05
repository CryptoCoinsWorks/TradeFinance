import os
import sqlite3
# from utils import constants as cst
from cryptography.fernet import Fernet


##### DATABASE Functions #####

def connection_to_db(db_path):
    create = False
    if not os.path.exists(db_path):
        create = True

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    if create:
        # create store table
        command1 = """CREATE TABLE user(user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_username TEXT, mail TEXT, password TEXT)"""
        cursor.execute(command1)
        cursor.close()
    return connection


def create_user(db_connection, user, mail, password):
    req = """INSERT INTO user (user_username, mail, password) VALUES (?,?,?)"""
    cursor = db_connection.cursor()
    cursor.execute(req, (user, mail, password))
    db_connection.commit()
    return cursor.lastrowid


def get_all_users(db_connection):
    req = """SELECT * FROM user"""
    cursor = db_connection.cursor()
    cursor.execute(req)
    return cursor.fetchall()


def find_user_login(db_connection, user, password, type_field="user_username"):
    req = """SELECT * FROM user WHERE {}= ? AND password= ?""".format(type_field)
    cursor = db_connection.cursor()
    cursor.execute(req, (user, password))
    return cursor.fetchone()


def get_user_by_id(db_connection, user_id):
    req = """SELECT * FROM user WHERE user_id=?"""
    cursor = db_connection.cursor()
    cursor.execute(req, (user_id,))
    return cursor.fetchone()


def sanity_check_mail_exist(db_connection, mail):
    req = """SELECT * FROM user WHERE mail = ?"""
    cursor = db_connection.cursor()
    cursor.execute(req, (mail,))
    data = cursor.fetchall()
    if not data:
        return True


##### CRYPTOGRAPHY Functions #####

def crypt_password(password):
    print(password.encode())
    cipher_suit = Fernet('pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='.encode())
    cipher_text = cipher_suit.encrypt(password.encode())
    return cipher_text

