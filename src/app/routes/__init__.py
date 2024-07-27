from flask import Blueprint
from src.app.routes.users import users

root = Blueprint("root", __name__)
root.register_blueprint(users, url_prefix="users")

from . import route
