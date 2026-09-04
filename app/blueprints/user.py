from flask import Blueprint, jsonify, request
from app.models import User
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, limiter

user_bp = Blueprint("user", __name__, url_prefix="/api/user")


@user_bp.route("/register", methods=["POST"])
def register():
    """
    Mendaftarkan pengguna baru.
    ---
    tags:
      - Pengguna
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      201:
        description: Registrasi berhasil.
      400:
        description: Validasi gagal (username/password tidak sesuai kriteria).
    """
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if len(username) < 3:
        return jsonify({"error": "Username minimal 3 karakter"}), 400
    if len(password) < 8:
        return jsonify({"error": "Password minimal 8 karakter"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username sudah digunakan"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registrasi berhasil"}), 201


@user_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    """
    Login ke dalam sistem.
    ---
    tags:
      - Pengguna
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login berhasil.
      401:
        description: Kredensial tidak valid.
    """
    data = request.get_json() or {}
    username = data.get("username", "")
    password = data.get("password", "")

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return (
            jsonify(
                {
                    "message": "Login berhasil",
                    "user_id": user.id,
                    "username": user.username,
                }
            ),
            200,
        )

    return jsonify({"error": "Kredensial tidak valid"}), 401


@user_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """
    Logout dari sistem (Membutuhkan Login).
    ---
    tags:
      - Pengguna
    responses:
      200:
        description: Logout berhasil.
      401:
        description: Belum login.
    """
    logout_user()
    return jsonify({"message": "Logout berhasil"}), 200


@user_bp.route("/me", methods=["GET"])
@login_required
def me():
    """
    Mendapatkan data profil pengguna yang sedang login.
    ---
    tags:
      - Pengguna
    responses:
      200:
        description: Berhasil mengembalikan data profil.
      401:
        description: Belum login.
    """
    return jsonify({"user_id": current_user.id, "username": current_user.username})
