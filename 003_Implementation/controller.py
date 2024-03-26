from fastapi import Response, status
import re
from argon2 import PasswordHasher

import db_operations as db_ops
from model import User

def email_exists(cursor, email):
    '''Returns True if the given email already exists in the database else False'''
    query = '''select exists(select 1 from users where email = %s) as email_found'''
    params = (email, )
    cursor.execute(query, params)
    result = cursor.fetchone()[0]
    return bool(result)

def mobile_exists(cursor, mobile):
    '''Returns True if the given mobile already exists in database else False'''
    query = '''select exists(select 1 from users where mobile = %s) as mobile_found'''
    params = (mobile, )
    cursor.execute(query, params)
    result = cursor.fetchone()[0]
    return bool(result)

def validate_password(password):
    '''Verify password must have atleast 1 digit, 1 capital letter, 1 small letter, 1 symbol'''
    if re.search("[0-9]", password) and \
       re.search("[a-z]", password) and \
       re.search("[A-Z]", password) and \
       (re.search("[\x21-\x2F]",password) or \
        re.search("[\x3A-\x40]",password) or \
        re.search("[\x5B-\x60]", password) or \
        re.search("[\x7B-\x7E]", password)):
        return True
    else:
        return False

def register_user_controller(user: User, response: Response):
    # Unpacking user details
    fname, lname, email, password, mobile = user.__dict__.values()

    # Converting details to lowercase to make below mentioned attributes case insensitive
    fname, lname, email = fname.lower(), lname.lower(), email.lower()

    # Password validation  
    password_validated = validate_password(password)
    if not password_validated:
        response.status_code = status.HTTP_400_BAD_REQUEST
        response.body = response.render('Invalid password format.')
        return response

    # DB connections
    conn = db_ops.db_connect()

    # Verify DB Connection
    if not db_ops.verify_db_connection(conn):
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        response.body = response.render("Database connection error.")
        return response
    
    with conn.cursor() as cursor:
        # Verify email presence in DB
        if email_exists(cursor, email):
            response.status_code = status.HTTP_409_CONFLICT
            response.body = response.render("Email address is already registered.")
            return response
    
        # Verify mobile presence in DB
        if mobile_exists(cursor, mobile):
            response.status_code = status.HTTP_409_CONFLICT
            response.body = response.render("Mobile is already registered.")
            return response

        # Generate hashed password using input password
        ph = PasswordHasher()
        hashed_password = ph.hash(password)

        # Insert new user in DB
        query = "INSERT INTO users VALUES(NULL, %s, %s, %s, %s, %s)"
        params = (fname, lname, email, hashed_password, mobile)
        cursor.execute(query, params)
        message = f"User with id={cursor.lastrowid} created."

    # Close DB connections
    db_ops.close_db_connection(conn)
    return {"message": message}


def get_users_controller(response: Response):
    '''Retrieve all user records'''
    
    users = []

    # Connect to DB
    conn = db_ops.db_connect()
    
    # Verify DB Connection    
    if not db_ops.verify_db_connection(conn):
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        response.body = response.render("Database connection error.")
        return response
    
    # Fetch existing users from DB
    with conn.cursor() as cursor:
        query = "SELECT * FROM users order by user_id desc"
        cursor.execute(query)
        users = cursor.fetchall()
    
    # Close DB connection
    db_ops.close_db_connection(conn)

    # Return the list of users
    return  {"users": users}
