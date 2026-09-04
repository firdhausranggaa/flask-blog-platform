from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("public.home"))

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash("Username sudah digunakan, silakan pilih yang lain.")
            return redirect(url_for("user.register"))

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash("Registrasi berhasil! Silakan login.")
        return redirect(url_for("user.login"))

    return render_template("register.html")


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("public.home"))

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("public.home"))
        else:
            flash("Login gagal. Periksa kembali username dan password Anda.")

    return render_template("login.html")


@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("public.home"))
