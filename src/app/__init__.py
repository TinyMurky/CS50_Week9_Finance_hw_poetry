"""
init flask here, and set session and other config
"""
import sys
for path in sys.path:
    print(path, "\n")

from flask import Flask
from flask_session import Session
from src.libs.common import get_abs_path
from src.app.routes import root
from src.libs.errors.register_error_handler import register_error_handlers
from src.constants.env import FLASK_SESSION_PATH

# Setting up flask
template_path = get_abs_path("templates")
static_path = get_abs_path("static")
app = Flask(__file__, template_folder=template_path, static_folder=static_path)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = FLASK_SESSION_PATH
Session(app)

register_error_handlers(app)
app.register_blueprint(root)
