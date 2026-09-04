from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Post
from flask_login import login_required, current_user
from app.extensions import db, limiter

post_bp = Blueprint("post", __name__, url_prefix="/api/post")


@post_bp.route("/create", methods=["POST"])
@login_required
@limiter.limit("10 per minute")
def create():
    data = request.get_json() or {}

    new_post = Post(
        title=data.get("title", ""),
        content=data.get("content", ""),
        category=data.get("category", ""),
        user_id=current_user.id,
    )

    db.session.add(new_post)
    db.session.commit()

    return (
        jsonify({"message": "Postingan berhasil diterbitkan!", "post_id": new_post.id}),
        201,
    )


@post_bp.route("/delete/<int:id>", methods=["DELETE"])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)

    if post.user_id == current_user.id:
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Postingan berhasil dihapus."}), 200

    return jsonify({"error": "Akses ditolak. Anda bukan penulis artikel ini."}), 403
