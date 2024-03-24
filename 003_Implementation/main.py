from fastapi import FastAPI, Response, status
from pydantic import BaseModel, Field, EmailStr
from passlib.context import CryptContext
import re

import db_operations as db_ops

class User(BaseModel):
    firstname: str = Field(pattern="[a-zA-Z]{3,10}")
    lastname: str = Field(pattern="[a-zA-Z]{3,10}")
    email: EmailStr
    mobile: str = Field(pattern="[0-9]{10}")
    password: str = Field(min_length=4, max_length=16)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

app = FastAPI()

def email_exists(cursor, email):
    query = '''select exists(select 1 from users where email = %s) as email_found'''
    params = (email, )
    cursor.execute(query, params)
    result = cursor.fetchone()[0]
    return bool(result)

def mobile_exists(cursor, mobile):
    query = '''select exists(select 1 from users where mobile = %s) as mobile_found'''
    params = (mobile, )
    cursor.execute(query, params)
    result = cursor.fetchone()[0]
    return bool(result)

def validate_password(password):
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

def insert_user_db(cursor, params):
    query = "INSERT INTO users VALUES(NULL, %s, %s, %s, %s, %s)"
    cursor.execute(query, params)


@app.post("/register", status_code=status.HTTP_200_OK)
def register(user: User, response: Response):
    fname, lname, email, mobile, password = user.__dict__.values()
    fname, lname, email = fname.lower(), lname.lower(), email.lower()
    
    conn = db_ops.db_connect()
    cursor = conn.cursor()

    # Check for email existence
    if email_exists(cursor, email):
        response.status_code = status.HTTP_409_CONFLICT
        response.body = response.render("Email address is already registered.")
        return response
    
    # Check for mobile existence
    if mobile_exists(cursor, mobile):
        response.status_code = status.HTTP_409_CONFLICT
        response.body = response.render("Mobile is already registered.")
        return response
    
    # Password validation  
    password_validated = validate_password(password)
    if not password_validated:
        response.status_code = status.HTTP_400_BAD_REQUEST
        response.body = response.render('Invalid password format.')
        return response

    # Generate hashed password using input password
    hashed_password = pwd_context.hash(password)

    # Insert new user in DB
    insert_user_db(cursor, (fname, lname, email, hashed_password, mobile))

    # Close DB connections
    cursor.close()
    conn.close()

    return {"message": f"User with id={cursor.lastrowid} created."}

@app.get("/users")
def get_users():
    '''Retrieve all user records'''
    conn = db_ops.db_connect()
    cursor = conn.cursor()
    query = "SELECT * FROM users order by user_id desc"
    cursor.execute(query)
    users = cursor.fetchall()
    return  {"users": users}
