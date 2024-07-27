from functools import wraps
from flask import session, redirect
from src.sql.sqlite import SQL
from src.libs.errors.error_classes import InvalidUserInputException


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        USER_LOGIN_URL = "/users/login"

        user_id = session.get("user_id")
        print("user_id", user_id, type(user_id))
        if not user_id or not isinstance(user_id, int):
            return redirect(USER_LOGIN_URL)

        # # to avoid pyLance angry about type
        # try:
        #     user_id = int(user_id)
        # except ValueError as exc:
        #     raise InvalidUserInputException from exc

        sql_imp = SQL()
        user = sql_imp.find_unique_user(user_id)

        print("user", user)
        print("user_id", user_id, type(user_id))

        if not user:
            return redirect(USER_LOGIN_URL)
        return f(*args, **kwargs)

    return decorated_function
