import os
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash


def get_abs_path(path: str):
    """
    get absolute path start from src
    """
    abs_path = Path(__file__).absolute().parent.parent

    return os.path.join(abs_path, path)


def usd(value: float):
    """
    format USD
    """
    return f"${value:,.2f}"


def hash_password(password: str):
    """
    hash password by werkzerg
    """
    return generate_password_hash(password)


def check_password(hashed_password: str, password: str):
    """
    check if password match hashed_password

    :hashed_password: password store in database
    :password: password user input
    """
    return check_password_hash(pwhash=hashed_password, password=password)
