from flask import Blueprint, render_template, redirect, url_for, request, flash, request
from flask_login.utils import logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Usuario
from flask_login import login_user
from database import db

auth = Blueprint("auth", __name__)


@auth.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    else:
        email = request.form.get("email")
        password = request.form.get("password")

        user = Usuario.query.filter_by(U_Email=email).first()

        # check if user actually exists
        # take the user supplied password, hash it, and compare it to the hashed password in database
        if not user or not check_password_hash(user.U_Senha, password):
            return render_template("signin.html", login_failed=True)

        login_user(user, remember=True)

        return redirect(url_for("main.index"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")

        user = Usuario.query.filter_by(U_Email=email).first()
        if (
            user
        ):  # if a user is found, we want to redirect back to register page so user can try again
            flash("Email address already exists")
            return redirect(url_for("auth.signup"))

        new_user = Usuario(
            U_Nome=fullname,
            U_Email=email,
            U_Senha=generate_password_hash(password, method="sha256"),
            U_Endereco="",
            U_Celular="",
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.signin"))


@auth.route("/signout")
def signout():
    logout_user()
    return redirect(url_for("main.index"))
