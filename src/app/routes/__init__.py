from flask import Blueprint
from src.app.routes.users import users
from src.app.routes.quote import quote
from src.app.routes.stock import stock

root = Blueprint("root", __name__)
root.register_blueprint(users, url_prefix="/users")
root.register_blueprint(quote, url_prefix="/quote")
root.register_blueprint(stock, url_prefix="/stock")

from . import route
