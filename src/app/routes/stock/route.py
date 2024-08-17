from flask import request, session, render_template, redirect
from libs.decorator import login_required
from src.app.routes.stock import stock
from src.libs.common import lookup, get_total_page, get_local_time, format_datetime
from src.sql.sqlite import sql_client
from src.libs.errors.error_classes import (
    InvalidUserInputException,
    NotEnoughMoney,
    NotEnoughShare,
)


@stock.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """
    Buy some stock
    """

    if "user_id" not in session or session["user_id"] is None:
        redirect("/")

    user_id = session["user_id"]

    if request.method == "POST":

        symbol = request.form.get("symbol")
        share = int(request.form.get("share") or -1)
        user_money = sql_client.find_unique_user(user_id)["cash"]

        if not symbol or share < 0:
            raise InvalidUserInputException

        symbol = symbol.upper()
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
@login_required
def sell():
    """
    Sell some stock
    """
    if "user_id" not in session or session["user_id"] is None:
        redirect("/")

    user_id = session["user_id"]

    if request.method == "POST":

        symbol = request.form.get("symbol")
        share = int(request.form.get("share") or -1)

        if not symbol or share < 0:
            raise InvalidUserInputException

        symbol = symbol.upper()

        share_from_db = sql_client.get_user_single_stock_shares(
            user_id=user_id, symbol=symbol
        )

        if share > share_from_db:
            raise NotEnoughShare

        current_quote: dict[str, float | str] | None = lookup(symbol=symbol)
        if current_quote is not None:
            symbol = str(current_quote["symbol"])
            price = float(current_quote["price"])

            print("symbol and price", symbol, price)
            idd = sql_client.sell(
                user_id=user_id, symbol=symbol, price=price, share=share
            )
            print("Sellaaa", idd)
        return redirect("/")
    return render_template("sell.html")


@stock.route("/history", methods=["GET"])
@login_required
def index():
    """
    POST to get quote from yahho

    POST: get symbol and redirect to  this route
    GET: render quote.html
    """

    user_id = session["user_id"]

    page_str = request.args.get("page")

    page = int(page_str) if page_str else 1

    limit = 10

    total_rows = sql_client.get_total_row_amount("transactions")
    total_pages = get_total_page(total_amount=total_rows, limit=limit)

    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    histories = (
        sql_client.find_many_history(page=page, limit=limit, user_id=user_id)
        if user_id
        else []
    )

    for history in histories:
        dt_time = get_local_time(history["timestamp"])
        history["time_str"] = format_datetime(dt_time)

    previous_disable = page <= 1
    next_disable = page >= total_pages
    # Pagination 需要 1. total page 2. current page 3. previous_disable: bool 4. next_disable: bool
    return render_template(
        "history.html",
        histories=histories,
        current_page=page,
        total_pages=total_pages,
        previous_disable=previous_disable,
        next_disable=next_disable,
    )
