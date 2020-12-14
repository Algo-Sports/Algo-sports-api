import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from algo_sports.blogs.tests.factories import PostFactory
from algo_sports.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestPermission:
    def test_is_owner_or_readonly(self):
        client = APIClient()

        users = [
            UserFactory(),
            UserFactory(),
        ]

        owner = users[0]
        another = users[1]

        post = PostFactory(user_id=owner)
        url = reverse("api:post-detail", kwargs={"pk": post.pk})
        views = [
            (
                client.put,
                {"title": "Hello", "content": "put method~"},
                status.HTTP_200_OK,
            ),
            (
                client.patch,
                {"title": "Hello2"},
                status.HTTP_200_OK,
            ),
            (
                client.delete,
                None,
                status.HTTP_204_NO_CONTENT,
            ),
        ]

        for method, param, sts in views:
            client.force_authenticate(user=another)
            response = method(url, param)
            assert response.status_code == status.HTTP_403_FORBIDDEN

        for method, param, sts in views:
            client.force_authenticate(user=owner)
            response = method(url, param)
            assert response.status_code == sts
