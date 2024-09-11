"""
Get env from .env then export
"""
import os
from dotenv import load_dotenv
from src.libs.common import create_path_if_not_exist, get_abs_path

load_dotenv()

PORT = os.getenv("PORT", "3000")
FLASK_SESSION_PATH = get_abs_path(os.getenv("FLASK_SESSION_PATH", "tmp/flask_session"))
SQLITE_PATH = get_abs_path(os.getenv("DATABASE_PATH", "tmp/database"))

print(f"PORT: {PORT}")
print(f"FLASK_SESSION_PATH: {FLASK_SESSION_PATH}")
print(f"SQLITE_PATH: {SQLITE_PATH}")

create_path_if_not_exist(FLASK_SESSION_PATH)
create_path_if_not_exist(SQLITE_PATH)

