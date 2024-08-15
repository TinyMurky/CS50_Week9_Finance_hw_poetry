"""
User login and register
"""

from flask import request, render_template, session, redirect, jsonify
from src.app.routes.users import users
from src.libs.errors.error_classes import (
    InvalidUserNameOrPassword,
    NotProvidePassword,
    NotProvideUserName,
)
from src.sql.sqlite import sql_client
from src.libs.common import check_password


@users.route("/login", methods=["GET", "POST"])
def login():
    """
    POST to submit login stuff
    GET to go to login page
    """
    if request.method == "POST":
        session.clear()

        username = request.form.get("username")

        if not username:
            raise NotProvideUserName

        password = request.form.get("password")

        if not password:
            raise NotProvidePassword

        user = sql_client.find_unique_user(username)

        if not user or not check_password(
            hashed_password=user["hash"], password=password
        ):
            raise InvalidUserNameOrPassword

        session["user_id"] = user["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@users.route("/logout", methods=["GET"])
def logout():
    """
    removed session and logout
    """

    session.clear()

    return redirect("/users/login")


@users.route("/register", methods=["GET", "POST"])
def register():
    """
    POST to submit register stuff
    GET to go to register page
    """
    if request.method == "POST":
        username = request.form.get("username")

        if not username:
            raise NotProvideUserName

        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not password or not confirm_password:
            raise NotProvidePassword

        if password != confirm_password:
            raise InvalidUserNameOrPassword

        sql_client.create_user(username=username, password=password)
        return redirect("/users/login")

    else:
        return render_template("register.html")


@users.route("/cash", methods=["GET"])
def get_user_cash():
    """
    Get user cash
    """
    result = {"cash": 0}
    try:
        user_id = session["user_id"]
    except KeyError:
        return jsonify(result)

    if not user_id:
        return jsonify(result)

    user = sql_client.find_unique_user(user_id)

    if not user:
        return jsonify(result)

    result["cash"] = user["cash"]

    return jsonify(result)
