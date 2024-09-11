"""
For getting quote from yahoo
"""

from flask import request, session, render_template, redirect
from src.libs.decorator import login_required
from src.app.routes.quote import quote
from src.libs.common import lookup, get_total_page, get_local_time, format_datetime
from src.sql.sqlite import sql_client


@quote.route("/", methods=["GET", "POST"])
@login_required
def index():
    """
    POST to get quote from yahho

    POST: get symbol and redirect to  this route
    GET: render quote.html
    """

    user_id = session["user_id"]
    if request.method == "POST":
        symbol = request.form.get("symbol")

        current_quote: dict[str, float | str] | None = None
        if symbol and user_id:
            current_quote = lookup(symbol=symbol)
            if current_quote is not None:
                symbol = str(current_quote["symbol"])
                price = float(current_quote["price"])
                sql_client.create_quote(
                    symbol=symbol,
                    price=price,
                    user_id=user_id,
                )

        return redirect("/quote")
    else:
        page_str = request.args.get("page")

        page = int(page_str) if page_str else 1

        limit = 10

        total_rows = sql_client.get_total_row_amount("quotes")
        total_pages = get_total_page(total_amount=total_rows, limit=limit)

        if page < 1:
            page = 1
        elif page > total_pages:
            page = total_pages

        quotes = (
            sql_client.find_many_quote(page=page, limit=limit, user_id=user_id)
            if user_id
            else []
        )

        for q in quotes:
            dt_time = get_local_time(q["timestamp"])
            q["time_str"] = format_datetime(dt_time)

        previous_disable = page <= 1
        next_disable = page >= total_pages
        # Pagination 需要 1. total page 2. current page 3. previous_disable: bool 4. next_disable: bool
        return render_template(
            "quote.html",
            quotes=quotes,
            current_page=page,
            total_pages=total_pages,
            previous_disable=previous_disable,
            next_disable=next_disable,
        )
