from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from app.extensions import db, migrate, login_manager, limiter
from app.models import User


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-key-rahasia"
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/flask_blog"

    app.config["SWAGGER"] = {"title": "Blogging Platform API", "uiversion": 3}
    Swagger(app)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    limiter.init_app(app)

    CORS(app, supports_credentials=True)

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({"error": "Akses ditolak, silakan login terlebih dahulu"}), 401

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.blueprints.public import public_bp
    from app.blueprints.user import user_bp
    from app.blueprints.post import post_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)

    return app
