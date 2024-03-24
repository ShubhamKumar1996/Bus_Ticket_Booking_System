from mysql.connector import connection

def db_connect():
    conn = connection.MySQLConnection(user='root', password = 'user', host='localhost', database='register_db')
    conn.autocommit = True
    return conn
