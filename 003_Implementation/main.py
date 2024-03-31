from fastapi import FastAPI, Response, status

from models import User
from controllers import controller

app = FastAPI()

@app.post("/register", status_code = status.HTTP_201_CREATED)
def register(user: User, response: Response):
    return controller.register_user(user, response)

@app.get("/users", status_code = status.HTTP_200_OK)
def get_users(response: Response):
    return controller.get_users(response)

@app.post('/users/login', status_code = status.HTTP_200_OK)
def user_login(user: User, response: Response):
    return controller.user_login(user, response)

