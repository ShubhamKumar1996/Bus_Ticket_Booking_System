from fastapi import FastAPI, Response

from model import User
from controller import get_users_controller, register_user_controller

app = FastAPI()

@app.post("/register")
def register(user: User, response: Response):
    return register_user_controller(user, response)

@app.get("/users")
def get_users(response: Response):
    return get_users_controller(response)
