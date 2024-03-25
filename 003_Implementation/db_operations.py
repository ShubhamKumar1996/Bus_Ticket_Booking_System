from mysql.connector import connection

config = {
    'user': 'root',
    'password': 'user',
    'host': 'localhost',
    'database': 'register_db',
    'autocommit': True
}

def db_connect():
    try:
        conn = None
        conn = connection.MySQLConnection(**config)
    except  Exception as e:
        print("Error connecting to MySQL", str(e))
    finally:
        return conn

def verify_db_connection(conn):
    if conn and conn.is_connected():
        return True
    return False

def close_db_connection(conn):
    conn.close()
