import os
from pathlib import Path


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
