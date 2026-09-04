from flask import Flask
from app.extensions import db, migrate, login_manager
from app.models import User


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-key-rahasia"
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/flask_blog"

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "user.login"

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
