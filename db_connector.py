from sqlite3 import Error
import pymysql
import yaml
from pypika import Table, Query
from user import User
import jsonpickle
from random import randint


def connect_DB():
    config = yaml.safe_load(open("config.yml"))
    connection = None
    try:
        connection = pymysql.connect(host=config['mysql']['host'],
                                     port=3306,
                                     user=config['mysql']['user'],
                                     passwd=config['mysql']['pass'],
                                     db=config['mysql']['name'])
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def unconnect_DB(cursor,connection):
    cursor.close()
    connection.close()


class Stock:

    #Get user_id and return user as object
    def get_user(user_id):
        connection = connect_DB()
        cursor = connection.cursor()
        users = Table('users')
        q = Query.from_(users).select('*').where(users.user_id == user_id)
        cursor.execute(str(q).replace('"',''))
        result = cursor.fetchall()
        unconnect_DB(cursor,connection)
        user = User(result[0]) if result else None
        print(user)
        return user if user else None

    #Get user, when user_id exists generate new id
    def create_user(user):
        user = jsonpickle.decode(user)
        user.id = Stock.validate_uniq_id(user.id)
        connection = connect_DB()
        cursor = connection.cursor()
        connection.autocommit(True)
        users = Table('users')
        q = Query.into(users).insert(user.id, user.name, user.date)
        cursor.execute(str(q).replace('"', ''))
        data = cursor
        unconnect_DB(cursor,connection)
        return user

    #Get user when user_id exists update
    def update_user(user):
        user = jsonpickle.decode(user)
        connection = connect_DB()
        cursor = connection.cursor()
        connection.autocommit(True)
        users = Table('users')
        q = Query.update(users).set(users.user_name, user.name).where(users.user_id == user.id)
        cursor.execute(str(q).replace('"', ''))
        data = cursor
        unconnect_DB(cursor, connection)
        return data

    #Get user  when user_id exists delete
    def delete_user(user_id):
        connection = connect_DB()
        cursor = connection.cursor()
        connection.autocommit(True)
        users = Table('users')
        q = Query.from_(users).delete().where(users.user_id == user_id)
        cursor.execute(str(q).replace('"', ''))
        data = cursor.rowcount
        unconnect_DB(cursor, connection)
        return data

    #Get user_id checks to see if there is a random new creator
    def validate_uniq_id(id):
        while Stock.get_user(id):
            id = randint(1, 999)
            Stock.get_user(id)
        return id
