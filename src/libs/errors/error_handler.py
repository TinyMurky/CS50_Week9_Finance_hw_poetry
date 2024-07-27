"""
List all error handling function
"""

from flask import render_template

from werkzeug.exceptions import HTTPException


def handle_exception_by_cat(error: HTTPException):
    """Render message as an apology to user."""

    code = error.code or 500
    message = error.description

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


# Normal handler should be like this
# def handle_bad_request(error):
#     response = jsonify({'message': error.description})
#     response.status_code = error.code
#     return response
