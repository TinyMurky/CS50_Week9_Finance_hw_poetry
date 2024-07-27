"""
Showing main home page
"""

from flask import render_template
from src.app.routes import root
from src.libs.decorator import login_required


@root.route("/")
@login_required
def home_page():
    return render_template("home.html")
