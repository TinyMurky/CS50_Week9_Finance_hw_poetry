import os
import datetime
import requests
import uuid
import pytz
import csv

from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request


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


def lookup(symbol):
    """Look up quote for symbol."""

    # Prepare API request
    symbol = symbol.upper()
    end = datetime.datetime.now(pytz.timezone("US/Eastern"))
    start = end - datetime.timedelta(days=7)

    # Yahoo Finance API
    url = (
        f"https://query1.finance.yahoo.com/v7/finance/download/{urllib.parse.quote_plus(symbol)}"
        f"?period1={int(start.timestamp())}"
        f"&period2={int(end.timestamp())}"
        f"&interval=1d&events=history&includeAdjustedClose=true"
    )

    # Query API
    try:
        response = requests.get(
            url,
            cookies={"session": str(uuid.uuid4())},
            headers={"Accept": "*/*", "User-Agent": request.headers.get("User-Agent")},
        )
        response.raise_for_status()

        # CSV header: Date,Open,High,Low,Close,Adj Close,Volume
        quotes = list(csv.DictReader(response.content.decode("utf-8").splitlines()))
        price = round(float(quotes[-1]["Adj Close"]), 2)
        return {"price": price, "symbol": symbol}
    except (KeyError, IndexError, requests.RequestException, ValueError):
        return None
