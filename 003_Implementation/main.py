from fastapi import FastAPI, Response, status
from pydantic import BaseModel, Field, EmailStr
import MySQLdb
import re

class User(BaseModel):
    firstname: str = Field(pattern="[a-zA-Z]{3,10}")
    lastname: str = Field(pattern="[a-zA-Z]{3,10}")
    email: EmailStr
    mobile: str = Field(pattern="[0-9]{10}")
    password: str = Field(min_length=4, max_length=16)

db_config = {
    'host': 'localhost',
    'user': 'root', 
    'password': 'user',
    'db': 'register_db'
}

conn = MySQLdb.connect(**db_config)
conn.autocommit = True

app = FastAPI()

def validate_password(password):
    if re.search("\d", password) and \
       re.search("[a-z]", password) and \
       re.search("[A-Z]", password) and \
       (re.search("[\x21-\x2F]",password) or \
        re.search("[\x3A-\x40]",password) or \
        re.search("[\x5B-\x60]", password) or \
        re.search("[\x7B-\x7E]", password)):
        return True
    else:
        return False


@app.post("/register", status_code=status.HTTP_200_OK)
def register(user: User, response: Response):
    fname, lname, email, mobile, password = user.__dict__.values()
    
    cursor = conn.cursor()

    # Check for email existence
    query = '''select exists(select 1 from users where email = %s) as email_found'''
    params = (email, )
    cursor.execute(query, params)
    email_exists = cursor.fetchone()[0]

    if email_exists:
        response.status_code = status.HTTP_409_CONFLICT
        response.body = response.render("Email address is already registered.")
        return response
    
    # Check for mobile existence
    query = '''select exists(select 1 from users where mobile = %s) as mobile_found'''
    params = (mobile, )
    cursor.execute(query, params)
    mobile_exists = cursor.fetchone()[0]
    if mobile_exists:
        response.status_code = status.HTTP_409_CONFLICT
        response.body = response.render("Mobile is already registered.")
        return response
    
    # Password validation  
    password_validated = validate_password(password)
    if not password_validated:
        response.status_code = status.HTTP_400_BAD_REQUEST
        response.body = response.render('Invalid password format.')
        return response

    fname = fname.lower()
    lname = lname.lower()
    # password = hashed password
    # Insert new user into the database

    query = "INSERT INTO users VALUES(NULL, %s, %s, %s, %s, %s)"
    params = tuple(user.__dict__.values())
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    return {"message": f"User with id={cursor.lastrowid} created."}

@app.get("/users")
def get_users():
    cursor = conn.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    
    users = cursor.fetchall()
    return  {"users": users}
