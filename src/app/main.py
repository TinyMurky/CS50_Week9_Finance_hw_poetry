"""
for poetry to start service
"""

from waitress import serve
from src.app import app

PORT = 3000


def start_dev():
    """
    start dev mode
    """
    app.run(debug=True, port=PORT)


def start_prod():
    """
    start prod mode
    """
    print(f"Production Server start on PORT: {PORT}")
    serve(app, port=PORT, host="0.0.0.0")
