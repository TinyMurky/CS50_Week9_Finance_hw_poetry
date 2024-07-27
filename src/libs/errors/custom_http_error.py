"""
1. Class CustomHttpException can customize HttpException
2. create_custom_http_exception can create  HttpException without extend Class
"""

from werkzeug.exceptions import HTTPException
from werkzeug.sansio.response import Response


class CustomHttpException(HTTPException):
    """
    Custom Exception if you don't want to use
    """

    def __init__(
        self,
        description: str | None = None,
        response: Response | None = None,
    ) -> None:
        if description is not None:
            self.description = description
        super().__init__(description=description, response=response)


def create_custom_http_exception(
    name, http_code, error_description, base_http_exception_class=None
):
    """
    use type to create a HTTPException, {"code": http_code, "description": error_description} means
    new class will be like

    class xxxException:
        code: http_code
        description: error_description

    Parameters
    ----------
    name: str
        the name of this exception, will be class name
    http_code: int
        like 400 ~500
    error_description: str
        describe your error
    base_http_exception_class: werkzeug.exceptions.HTTPException
        let this class extend certain HTTPException like werkzeug.exceptions.HTTPException.BadRequest
        it will be basic werkzeug.exceptions.HTTPException if not provided
    """
    if not base_http_exception_class:
        base_http_exception_class = HTTPException

    return type(
        name,
        (base_http_exception_class,),
        {"code": http_code, "description": error_description},
    )
