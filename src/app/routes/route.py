"""
Showing main home page
"""

from flask import render_template, session, redirect
from src.app.routes import root
from src.libs.decorator import login_required
from src.sql.sqlite import sql_client
from src.libs.common import number_to_money


@root.route("/")
@login_required
def home_page():
    """
    home page for dash board
    """
    user_id = session.get("user_id")

    if not user_id:
        return redirect("/users/login")

    total_cash = sql_client.find_unique_user(user_id)["cash"]

    portfolios = sql_client.get_portfolio(user_id=user_id)

    total_amount_of_portfolio = sum(
        int(portfolio["total_price"]) for portfolio in portfolios
    )

    total_asset = total_cash + total_amount_of_portfolio

    for portfolio in portfolios:
        total_price = portfolio["total_price"]
        portfolio["total_price"] = number_to_money(total_price)

        avg_price = portfolio["avg_price"]
        portfolio["avg_price"] = number_to_money(avg_price)

    total_cash = number_to_money(total_cash)
    total_asset = number_to_money(total_asset)
    print(portfolios)
    return render_template(
        "home.html",
        total_cash=total_cash,
        portfolios=portfolios,
        total_amount=total_amount_of_portfolio,
        total_asset=total_asset,
    )
