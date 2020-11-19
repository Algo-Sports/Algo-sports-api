import pytest

from algo_sports.blogs.tests.factories import BlogFactory, CommentFactory, PostFactory
from algo_sports.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestBlogAppModelMethods:
    def test_blogapp(self):
        blog = BlogFactory()
        post = PostFactory(blog_id=blog)
        comments = CommentFactory.create_batch(
            20,
            post_id=post,
            user_id=post.user,
        )

        for c in post.get_comments():
            assert c in comments

        comment = comments[0]
        recomments = CommentFactory.create_batch(
            20,
            parent_id=comment,
            user_id=UserFactory(),
        )

        assert post == comment.post
        assert blog == post.blog

        for c in comment.get_childs():
            assert c in recomments
            assert c.parent == comment
