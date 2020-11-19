from django_filters import rest_framework as filters
from django_filters.filters import CharFilter

from .models import Blog, Comment, Post


class BlogFilter(filters.FilterSet):
    class Meta:
        model = Blog
        fields = (
            "category",
            "permission",
        )


class PostFilter(filters.FilterSet):
    blog = CharFilter(field_name="blog_id__category")

    class Meta:
        model = Post
        fields = ("title",)


class CommentFilter(filters.FilterSet):
    class Meta:
        model = Comment
        fields = (
            "post_id",
            "parent_id",
        )
