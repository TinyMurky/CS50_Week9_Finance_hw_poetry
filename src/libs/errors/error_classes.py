"""
List all customer Exception

error_exception_mapper is mapper
"""

from src.libs.errors.custom_http_error import create_custom_http_exception
from werkzeug import exceptions


DatabaseReadFailException = create_custom_http_exception(
    "DatabaseReadFailException",
    500,
    "Can't read from database",
    exceptions.InternalServerError,
)

DatabaseCreateFailException = create_custom_http_exception(
    "DatabaseCreateFailException",
    500,
    "Can't Create from database",
    exceptions.InternalServerError,
)

DatabaseUpdateFailException = create_custom_http_exception(
    "DatabaseUpdateFailException",
    500,
    "Can't Update from database",
    exceptions.InternalServerError,
)

InvalidUserInputException = create_custom_http_exception(
    "InvalidUserInputException", 400, "Your input is invalid", exceptions.BadRequest
)

NotEnoughMoney = create_custom_http_exception(
    "NotEnoughMoney",
    400,
    "There is not sufficient amount in your account",
    exceptions.BadRequest,
)

NotProvideUserName = create_custom_http_exception(
    "NotProvideUserName", 403, "You must provide username", exceptions.Forbidden
)

NotProvidePassword = create_custom_http_exception(
    "NotProvidePassword", 403, "You must provide password", exceptions.Forbidden
)

InvalidUserNameOrPassword = create_custom_http_exception(
    "InvalidUserNameOrPassword", 403, "Bad Username or password", exceptions.Forbidden
)

InvalidDevInputArgument = create_custom_http_exception(
    "InvalidDevInputArgument", 500, "Dev use bad input", exceptions.InternalServerError
)

NoSuchUser = create_custom_http_exception(
    "NoSuchUser", 404, "This user isn't existed", exceptions.NotFound
)

NotEnoughMoney = create_custom_http_exception(
    "NotEnoughMoney", 400, "Sorry, you don't have enough money", exceptions.BadRequest
)

NotEnoughShare = create_custom_http_exception(
    "NotEnoughShare",
    400,
    "Sorry, you don't have enough share to sell",
    exceptions.BadRequest,
)

error_exception_mapper = {
    "DatabaseReadFailException": DatabaseReadFailException,
    "DatabaseCreateFailException": DatabaseCreateFailException,
    "DatabaseUpdateFailException": DatabaseUpdateFailException,
    "InvalidUserInputException": InvalidUserInputException,
    "NotEnoughMoney": NotEnoughMoney,
    "NotProvideUserName": NotProvideUserName,
    "NotProvidePassword": NotProvidePassword,
    "InvalidUserNameOrPassword": InvalidUserInputException,
    "InvalidDevInputArgument": InvalidDevInputArgument,
}
