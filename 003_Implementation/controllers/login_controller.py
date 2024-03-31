from fastapi import Response, status
from argon2 import PasswordHasher, exceptions
from models import User

from db_operations import DbConnector

def get_hashed_password(cursor, email):
    query = '''SELECT password FROM users WHERE email = %s'''
    params = (email,)
    cursor.execute(query, params)
    result = cursor.fetchone()
    if result is None:
        return None
    else:
        return result[0]

def update_password(cursor, email, hashed_password):
    query = '''UPDATE users SET password=%s WHERE email=%s'''
    params = (hashed_password, email)
    cursor.execute(query, params)

def user_login(user: User, response: Response):
    
    # Unpack email and password from request body
    email, password = user.email.lower(), user.password

    # Create connection to DB
    dbconnector = DbConnector()
    conn = dbconnector.create_connection()

    # Verify email exists in DB
    if not dbconnector.verify_connection():
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        response.body = response.render("Database Connection Error.")
        return response
    
    with conn.cursor() as cursor:

        try:
            # Fetch hashed password for email
            hashed_password = get_hashed_password(cursor, email)

            if not hashed_password:
                response.status_code = status.HTTP_401_UNAUTHORIZED
                response.body = response.render("Unregistered Email Address.")
                return response
        
            # Password comparision
            hasher = PasswordHasher()
            hasher.verify(hashed_password, password)
            if hasher.check_needs_rehash(hashed_password):
                hashed_password = hasher.hash(password)
                update_password(cursor, email, hashed_password)

        except (exceptions.VerifyMismatchError, exceptions.VerificationError, exceptions.InvalidHashError) as err:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            response.body = response.render(str(err))
            return response

        
    response.body = response.render("Successful Login")
    dbconnector.close_connection()
