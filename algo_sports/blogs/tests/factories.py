from factory import Faker, fuzzy
from factory.declarations import SubFactory
from factory.django import DjangoModelFactory

from algo_sports.blogs.models import Blog, Comment, Post
from algo_sports.users.tests.factories import UserFactory


class BlogFactory(DjangoModelFactory):
    category = Faker("word")
    print(Blog.permission_choices)
    permission = fuzzy.FuzzyChoice(Blog.permission_choices())
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
