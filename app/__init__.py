from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from werkzeug.exceptions import HTTPException
from app.extensions import db, migrate, limiter, jwt, ma


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-key-rahasia"
    app.config["JWT_SECRET_KEY"] = (
        "jwt-super-rahasia-jangan-bocor"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/flask_blog"

    swagger_config = {
        "headers": [],
        "specs": [{"endpoint": "apispec_1", "route": "/apispec_1.json"}],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
        "title": "Blogging Platform API",
        "uiversion": 3,
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Ketikkan token dengan format: Bearer <access_token>",
            }
        },
        "security": [{"Bearer": []}],
    }
    Swagger(app, config=swagger_config)

    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)

    CORS(app, supports_credentials=True)

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({"error": "Akses ditolak, token JWT tidak ditemukan di header"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"error": "Token JWT tidak valid atau telah dimodifikasi"}), 401

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return jsonify({"error": e.name, "description": e.description}), e.code
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

    from app.blueprints.public import public_bp
    from app.blueprints.user import user_bp
    from app.blueprints.post import post_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)

    return app
