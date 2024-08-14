from flask import request, session, render_template, redirect
from src.app.routes.stock import stock
from src.libs.common import lookup, get_total_page, get_local_time, format_datetime
from src.sql.sqlite import sql_client


@stock.route("/buy", methods=["GET", "POST"])
def buy():
    return "a"


@stock.route("/sell", methods=["GET", "POST"])
def sell():
    return "a"
