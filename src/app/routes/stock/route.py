from flask import request, session, render_template, redirect
from src.app.routes.stock import stock
from src.libs.common import lookup, get_total_page, get_local_time, format_datetime
from src.sql.sqlite import sql_client
from src.libs.errors.error_classes import InvalidUserInputException, NotEnoughMoney


@stock.route("/buy", methods=["GET", "POST"])
def buy():

    if "user_id" not in session or session["user_id"] is None:
        redirect("/")

    user_id = session["user_id"]

    if request.method == "POST":

        symbol = request.form.get("symbol")
        share = int(request.form.get("share") or -1)
        user_money = sql_client.find_unique_user(user_id)["cash"]

        if not symbol or share < 0:
            raise InvalidUserInputException

        current_quote: dict[str, float | str] | None = lookup(symbol=symbol)
        if current_quote is not None:
            symbol = str(current_quote["symbol"])
            price = float(current_quote["price"])

            total_price = price * share

            if total_price > user_money:
                raise NotEnoughMoney

            sql_client.buy(user_id=user_id, symbol=symbol, price=price, share=share)
        return redirect("/")
    return render_template("buy.html")


@stock.route("/sell", methods=["GET", "POST"])
def sell():
    return "a"
