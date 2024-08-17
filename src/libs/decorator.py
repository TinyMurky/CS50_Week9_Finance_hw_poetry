from functools import wraps
from flask import session, redirect
from src.sql.sqlite import sql_client


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        USER_LOGIN_URL = "/users/login"

        user_id = session.get("user_id")
        if not user_id or not isinstance(user_id, int):
            return redirect(USER_LOGIN_URL)

        # # to avoid pyLance angry about type
        # try:
        #     user_id = int(user_id)
        # except ValueError as exc:
        #     raise InvalidUserInputException from exc

        user = sql_client.find_unique_user(user_id)

        if not user:
            return redirect(USER_LOGIN_URL)
        return f(*args, **kwargs)

    return decorated_function
