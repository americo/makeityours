from audioop import cross
from crypt import methods
from flask import (
    request,
    Blueprint,
    jsonify,
    make_response,
)
from sqlalchemy import null
from main import ADMIN_TOKEN
from models import (
    Carrinho,
    Pedido,
    Comentario,
)
from flask_cors import CORS, cross_origin
from flask_login import login_required, current_user
from database import db
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

api = Blueprint("api", __name__)


@api.route("/api")
def hello():
    return jsonify({"message": f"The API is still under construction!"})


@api.route("/api/v1")
def v1Hello():
    return jsonify(
        {
            "message": f"The API is still under construction!",
            "version": "1.0",
            "endpoints": ["/admin"],
        }
    )


@api.route("/api/v2")
def v2Hello():
    return jsonify(
        {
            "message": f"The API is still under construction!",
            "version": "2.0",
            "endpoints": ["/admin"],
        }
    )


@api.route("/api/v3")
def v3Hello():
    return jsonify(
        {
            "message": f"The API is still under construction!",
            "version": "2.0",
            "endpoints": ["/admin"],
        }
    )


@api.route("/api/v1/admin")
def v1Admin():
    ADMIN_TOKEN = "C1C224B03CD9BC7B6A86D77F5DACE40191766C485CD55DC48CAF9AC873335D6F"
    req_origin = request.headers.get("Origin")
    res = make_response(
        jsonify(
            {
                "token": f"{ADMIN_TOKEN}",
            }
        ),
        {"Access-Control-Allow-Credentials": True},
    )
    res.headers["Access-Control-Allow-Origin"] = str(req_origin)
    res.headers["Access-Control-Allow-Credentials"] = "true"
    res.headers["Access-Control-Request-Method"] = "GET"

    if req_origin:
        return res
    else:
        return jsonify({"message": "this origin is not allowed"})


@api.route("/api/v2/admin")
def v2Admin():
    ADMIN_TOKEN = "C1C224B03CD9BC7B6A86D77F5DACE40191766C485CD55DC48CAF9AC873335D6F"
    req_origin = request.headers.get("Origin")
    res = make_response(
        jsonify(
            {
                "token": f"{ADMIN_TOKEN}",
            }
        ),
        {"Access-Control-Allow-Credentials": True},
    )
    res.headers["Access-Control-Allow-Origin"] = str(req_origin)
    res.headers["Access-Control-Allow-Credentials"] = "true"
    res.headers["Access-Control-Request-Method"] = "GET"

    if (
        req_origin == "http://thebughunter.dev"
        or req_origin == "https://thebughunter.dev"
    ):
        return res
    elif req_origin == "null":
        return res
    else:
        return jsonify(
            {
                "message": "the origin http(s)://thebughunter.dev is the only one allowed!"
            }
        )


@api.route("/api/v3/admin")
def v3Admin():
    ADMIN_TOKEN = "C1C224B03CD9BC7B6A86D77F5DACE40191766C485CD55DC48CAF9AC873335D6F"
    req_origin = request.headers.get("Origin")
    res = make_response(
        jsonify(
            {
                "token": f"{ADMIN_TOKEN}",
            }
        ),
        {"Access-Control-Allow-Credentials": True},
    )
    res.headers["Access-Control-Allow-Origin"] = str(req_origin)
    res.headers["Access-Control-Allow-Credentials"] = "true"
    res.headers["Access-Control-Request-Method"] = "GET"

    ALLOWED_ORIGIN = "http://thebughunter.dev"
    ALLOWED_ORIGIN_2 = "https://thebughunter.dev"

    if req_origin:
        if ALLOWED_ORIGIN in req_origin or ALLOWED_ORIGIN_2 in req_origin:
            return res
        else:
            return jsonify(
                {
                    "message": "the origin http(s)://thebughunter.dev is the only one allowed!"
                }
            )
    else:
        return jsonify(
            {
                "message": "the origin http(s)://thebughunter.dev is the only one allowed!"
            }
        )
