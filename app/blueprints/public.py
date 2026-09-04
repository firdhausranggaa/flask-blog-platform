from flask import Blueprint, jsonify, request
from app.models import Post

public_bp = Blueprint("public", __name__)


@public_bp.route("/api/posts", methods=["GET"])
def get_posts():
    category = request.args.get("category")

    if category:
        posts = (
            Post.query.filter_by(category=category)
            .order_by(Post.date_posted.desc())
            .all()
        )
    else:
        posts = Post.query.order_by(Post.date_posted.desc()).all()

    result = []
    for post in posts:
        result.append(
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "category": post.category,
                "author": post.author.username,
                "date_posted": post.date_posted.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return jsonify(result)
