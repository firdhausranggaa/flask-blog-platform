from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import Post
from flask_login import login_required, current_user

post_bp = Blueprint("post", __name__, url_prefix="/post")


@post_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        title = request.form.get("title", "")
        content = request.form.get("content", "")
        category = request.form.get("category", "")

        new_post = Post(title=title, content=content, category=category, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()

        flash("Postingan berhasil diterbitkan!")
        return redirect(url_for("public.home"))

    return render_template("create_post.html")


@post_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    # Memastikan hanya pembuat artikel yang bisa menghapusnya
    if post.user_id == current_user.id:
        db.session.delete(post)
        db.session.commit()
        flash("Postingan berhasil dihapus.")
    return redirect(url_for("public.home"))
