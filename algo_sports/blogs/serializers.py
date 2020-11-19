from rest_framework import serializers

from algo_sports.users.serializers import UsernameSerializer

from .models import Blog, Comment, Post


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "category",
            "permission",
            "description",
        ]


class PostSerializer(serializers.ModelSerializer):
    user = UsernameSerializer(read_only=True)
    blog = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "user",
            "blog",
            "content",
            "created_at",
            "updated_at",
        ]


class ReCommentSerializer(serializers.ModelSerializer):
    user = UsernameSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = ["post_id", "user_id", "parent_id"]


class CommentSerializer(serializers.ModelSerializer):
    user = UsernameSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    recomments = ReCommentSerializer(source="get_childs", many=True, required=False)

    class Meta:
        model = Comment
        exclude = ["post_id", "user_id", "parent_id"]
