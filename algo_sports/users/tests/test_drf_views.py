import pytest
from django.urls.base import reverse
from rest_framework.test import APIClient, APIRequestFactory

from algo_sports.users.serializers import UserSerializer
from algo_sports.users.tests.factories import UserFactory
from algo_sports.users.views import UserViewSet

pytestmark = pytest.mark.django_db


class TestUserViewSet:
    def test_get_queryset(self):
        view = UserViewSet()

        user = UserFactory()

        rf = APIRequestFactory()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self):
        client = APIClient()

        users = UserFactory.create_batch(10)

        user_me_url = reverse("api:user-me")
        for user in users:
            client.force_authenticate(user=user)
            response = client.get(user_me_url)

            serializer = UserSerializer(instance=user)
            assert serializer.data == response.json()
