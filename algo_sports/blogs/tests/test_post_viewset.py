import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from algo_sports.blogs.tests.factories import BlogFactory, PostFactory
from algo_sports.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestPostViewSet:
    def test_add_comment(self):
        client = APIClient()

        BlogFactory.create_batch(100)

        user = UserFactory()

        client.force_authenticate(user=user)
        post = PostFactory(user_id=user)

        url = reverse("api:post-add-comment", kwargs={"pk": post.pk})
        response = client.post(url, data={"content": "Hello! This is Comment"})
        assert response.status_code == status.HTTP_201_CREATED

        user2 = UserFactory()
        client.force_authenticate(user=user2)
        response = client.post(url, data={"content": "Hello! This is Comment"})
        assert response.status_code == status.HTTP_201_CREATED
