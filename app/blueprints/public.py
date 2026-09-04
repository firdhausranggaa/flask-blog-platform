from flask import Blueprint, render_template, request
from app.models import Post

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def home():
    category = request.args.get("category")

    if category:
        posts = (
            Post.query.filter_by(category=category)
            .order_by(Post.date_posted.desc())
            .all()
        )
    else:
        posts = Post.query.order_by(Post.date_posted.desc()).all()

    return render_template("home.html", posts=posts)
