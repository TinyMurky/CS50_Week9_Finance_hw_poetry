from flask import Blueprint
from src.app.routes.users import users
from src.app.routes.quote import quote

root = Blueprint("root", __name__)
root.register_blueprint(users, url_prefix="/users")
root.register_blueprint(quote, url_prefix="/quote")

from . import route
