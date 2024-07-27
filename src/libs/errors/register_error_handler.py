from flask import Flask
from src.libs.errors import error_handler
from src.libs.errors.error_classes import error_exception_mapper


def register_error_handlers(app: Flask):
    """
    Register all error to error handler
    """

    for _, exception in error_exception_mapper.items():
        app.register_error_handler(exception, error_handler.handle_exception_by_cat)
