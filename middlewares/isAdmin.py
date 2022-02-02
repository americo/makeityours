from tracemalloc import start
from flask import request
from werkzeug.wrappers import Request, Response, ResponseStream


class isAdmin:
    """
    Verify if user is admins
    """

    def __init__(self, app):
        self.app = app
        self.adminToken = (
            "C1C224B03CD9BC7B6A86D77F5DACE40191766C485CD55DC48CAF9AC873335D6F"
        )

    def __call__(self, environ, start_response):
        request = Request(environ)
        _adminToken = request.cookies.get("adminToken")
        if _adminToken != self.adminToken:
            environ["token"] = {
                "token": "C1C224B03CD9BC7B6A86D77F5DACE40191766C485CD55DC48CAF9AC873335D6F"
            }
            return self.app(environ, start_response)

        res = Response(u"Authorization failed", mimetype="text/plain", status=401)
        return res(environ, start_response)
