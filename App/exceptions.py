from fastapi import Request
from fastapi.responses import RedirectResponse

class NotAuthenticatedException(Exception):
    """
    Exception to trigger when the user is not authenticated.
    """
    pass

def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    """
    Redirect the user to the login page if not logged in
    """
    return RedirectResponse(url="/user/signin")


def include_app(app):
    """
    Creates the exception handler to redirect the user to the login when not authenticated.
    """
    app.add_exception_handler(NotAuthenticatedException, auth_exception_handler)
