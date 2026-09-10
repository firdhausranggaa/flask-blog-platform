from flask_marshmallow import Marshmallow
from app.models import Post, User

ma = Marshmallow()


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("password",)


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        include_fk = True
        load_instance = True

    author = ma.Nested(UserSchema, only=("username",))


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
