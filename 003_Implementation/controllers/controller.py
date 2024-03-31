from fastapi import Response

from models import User
from controllers import registration_controller, user_controller, login_controller

def register_user(user: User, response: Response):
    return registration_controller.register_user(user, response)

def get_users(response: Response):
    return user_controller.get_users(response)

def user_login(user: User, response: Response):
    return login_controller.user_login(user, response)
