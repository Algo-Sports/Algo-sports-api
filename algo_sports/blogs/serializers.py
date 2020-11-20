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

    def to_representation(self, instance):
        """ Deleted comment의 전송되는 필드 제한 """
        representation = super().to_representation(instance)
        if instance.deleted:
            exclude_fields = ("user", "content")
            for field in exclude_fields:
                representation.pop(field)
        return representation


class CommentSerializer(serializers.ModelSerializer):
    user = UsernameSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        exclude = ["post_id", "user_id", "parent_id"]

    def to_representation(self, instance):
        """ Deleted comment의 전송되는 필드 제한 """
        representation = super().to_representation(instance)
        if instance.deleted:
            exclude_fields = ("user", "content")
            for field in exclude_fields:
                representation.pop(field)
        return representation
