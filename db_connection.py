import pymysql.cursors
import gc

db_name = 'MyNewORM'
# тут мои данные, так что меняй

def get_connection():
    # тут мои данные, так что меняй
    return pymysql.connect(host='localhost', user='root', password='lumen23291633', db = db_name, cursorclass=pymysql.cursors.DictCursor)

def init_db(host, user, password):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            query = 'CREATE DATABASE IF NOT EXISTS `%s`'
            cursor.execute(query % (db_name))

        connection.commit()

    finally:
        connection.close()
        gc.collect()

