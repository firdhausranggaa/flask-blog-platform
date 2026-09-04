from flask import Blueprint, jsonify, request, redirect
from app.models import Post

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def index():
    """Mengalihkan halaman utama (/) langsung ke halaman Swagger"""
    return redirect("/apidocs")


@public_bp.route("/api/posts", methods=["GET"])
def get_posts():
    """
    Mengambil daftar artikel blog dengan fitur paginasi dan pencarian.
    ---
    tags:
      - Publik
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: Nomor halaman.
      - name: per_page
        in: query
        type: integer
        required: false
        default: 5
        description: Jumlah artikel per halaman.
      - name: category
        in: query
        type: string
        required: false
        description: Filter berdasarkan kategori artikel.
      - name: search
        in: query
        type: string
        required: false
        description: Kata kunci untuk mencari judul atau konten.
    responses:
      200:
        description: Daftar artikel berhasil dikembalikan beserta metadata.
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)
    category = request.args.get("category")
    search = request.args.get("search")

    query = Post.query

    if category:
        query = query.filter_by(category=category)

    if search:
        query = query.filter(
            Post.title.ilike(f"%{search}%") | Post.content.ilike(f"%{search}%")
        )

    paginated_posts = query.order_by(Post.date_posted.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    result = []
    for post in paginated_posts.items:
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

    return (
        jsonify(
            {
                "data": result,
                "meta": {
                    "total_items": paginated_posts.total,
                    "total_pages": paginated_posts.pages,
                    "current_page": paginated_posts.page,
                    "per_page": paginated_posts.per_page,
                    "has_next": paginated_posts.has_next,
                    "has_prev": paginated_posts.has_prev,
                },
            }
        ),
        200,
    )
