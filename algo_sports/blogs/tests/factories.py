from factory import Faker, Sequence, fuzzy
from factory.declarations import SubFactory
from factory.django import DjangoModelFactory

from algo_sports.blogs.models import Blog, Comment, Post
from algo_sports.users.tests.factories import UserFactory
from algo_sports.utils.choices import PermissionChoices


class BlogFactory(DjangoModelFactory):
    category = Sequence(lambda n: f"Category {n}")
    permission = fuzzy.FuzzyChoice(PermissionChoices.values)
    description = Faker("sentence")

    class Meta:
        model = Blog


class PostFactory(DjangoModelFactory):
    title = Faker("sentence")
    user_id = SubFactory(UserFactory)
    blog_id = SubFactory(BlogFactory)

    content = Faker("sentence")

    class Meta:
        model = Post


class CommentFactory(DjangoModelFactory):
    post_id = SubFactory(PostFactory)
    user_id = SubFactory(UserFactory)

    content = Faker("sentence")

    class Meta:
        model = Comment
