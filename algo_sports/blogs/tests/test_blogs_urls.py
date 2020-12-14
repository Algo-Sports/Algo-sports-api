import pytest
from django.urls import resolve, reverse

from algo_sports.blogs.tests.factories import BlogFactory, CommentFactory, PostFactory
from algo_sports.utils.test.compare_url import compare_url

pytestmark = pytest.mark.django_db


def test_blog_url():
    blog = BlogFactory()
    lookup_field = "category"
    lookup_value = blog.category

    # reverse url
    assert compare_url(
        reverse("api:blog-detail", kwargs={lookup_field: lookup_value}),
        f"/api/blogs/{lookup_value}/",
    )
    assert compare_url(reverse("api:blog-list"), "/api/blogs/")
    assert compare_url(
        reverse("api:blog-add-post", kwargs={lookup_field: lookup_value}),
        f"/api/blogs/{lookup_value}/add_post/",
    )

    # resolve view name
    assert resolve(f"/api/blogs/{lookup_value}/").view_name == "api:blog-detail"
    assert resolve("/api/blogs/").view_name == "api:blog-list"
    assert (
        resolve(f"/api/blogs/{lookup_value}/add_post/").view_name == "api:blog-add-post"
    )


def test_post_url():
    post = PostFactory()
    lookup_field = "pk"
    lookup_value = post.pk

    # reverse url
    assert compare_url(
        reverse("api:post-detail", kwargs={lookup_field: lookup_value}),
        f"/api/posts/{lookup_value}/",
    )
    assert compare_url(reverse("api:post-list"), "/api/posts/")
    assert compare_url(
        reverse("api:post-add-comment", kwargs={lookup_field: lookup_value}),
        f"/api/posts/{lookup_value}/add_comment/",
    )

    # resolve view name
    assert resolve(f"/api/posts/{lookup_value}/").view_name == "api:post-detail"
    assert resolve("/api/posts/").view_name == "api:post-list"
    assert (
        resolve(f"/api/posts/{lookup_value}/add_comment/").view_name
        == "api:post-add-comment"
    )


def test_comment_url():
    comment = CommentFactory()
    lookup_field = "pk"
    lookup_value = comment.pk

    # reverse url
    assert compare_url(
        reverse("api:comment-detail", kwargs={lookup_field: lookup_value}),
        f"/api/comments/{lookup_value}/",
    )
    assert compare_url(reverse("api:comment-list"), "/api/comments/")
    assert compare_url(
        reverse("api:comment-add-recomment", kwargs={lookup_field: lookup_value}),
        f"/api/comments/{lookup_value}/add_recomment/",
    )
    assert compare_url(
        reverse("api:comment-add-recomment", kwargs={lookup_field: lookup_value}),
        f"/api/comments/{lookup_value}/add_recomment/",
    )

    # resolve view name
    assert resolve(f"/api/comments/{lookup_value}/").view_name == "api:comment-detail"
    assert resolve("/api/comments/").view_name == "api:comment-list"
    assert (
        resolve(f"/api/comments/{lookup_value}/add_recomment/").view_name
        == "api:comment-add-recomment"
    )
