import pytest
from django.test import RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from algo_sports.blogs.models import Blog
from algo_sports.blogs.tests.factories import BlogFactory
from algo_sports.blogs.views import BlogViewSet
from algo_sports.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestBlogVIewSet:
    def test_get_queryset(self, rf: RequestFactory):
        # 기본 세팅
        view = BlogViewSet()
        request = rf.get("/fake-url/")

        users = [
            UserFactory(is_superuser=True),
            UserFactory(is_staff=True),
            UserFactory(),
        ]

        BlogFactory.create_batch(100)

        for user in users:
            request.user = user
            view.request = request
            permissions = view.get_queryset().values_list("permission", flat=True)

            for permission in permissions:
                assert permission <= user.level

    def test_list(self):
        client = APIClient()

        users = [
            UserFactory(),
            UserFactory(is_staff=True),
            UserFactory(is_superuser=True),
        ]

        BlogFactory.create_batch(100)

        for user in users:
            client.force_authenticate(user=user)
            blog_list_url = reverse("api:blog-list")
            response = client.get(blog_list_url)

            blogs = Blog.objects.all().filter(permission__lte=user.level).count()
            allowed_blogs = len(response.json())

            assert blogs == allowed_blogs

    def test_add_post(self):
        client = APIClient()

        users = [
            UserFactory(),
            UserFactory(is_staff=True),
            UserFactory(is_superuser=True),
        ]

        BlogFactory.create_batch(100)

        for user in users:
            client.force_authenticate(user=user)
            blogs = Blog.objects.all()
            for blog in blogs:
                url = reverse("api:blog-add-post", kwargs={"category": blog.category})
                response = client.post(
                    url,
                    data={"title": "Hello", "content": "How are you?"},
                )
                if blog.permission <= user.level:
                    # 블로그 권한이 더 낮을 시 201
                    assert response.status_code == status.HTTP_201_CREATED
                else:
                    # 블로그 권한이 더 높을 시 쿼리 불가 404
                    assert response.status_code == status.HTTP_404_NOT_FOUND
