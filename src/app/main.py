"""
for poetry to start service
"""

from waitress import serve
from src.app import app
from src.constants.env import PORT


def start_dev():
    """
    start dev mode
    """
    app.run(debug=True, port=int(PORT))


def start_prod():
    """
    start prod mode
    """

    print(f"Production Server start on PORT: {PORT}")

    serve(app, port=PORT, host="0.0.0.0")

if __name__ == "__main__":
    start_prod()
