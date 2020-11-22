import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory

from algo_sports.codes.models import UserCode
from algo_sports.codes.tests.factories import UserCodeFactory
from algo_sports.codes.views import UserCodeViewSet
from algo_sports.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestUserCodeViewSet:
    def test_get_queryset(self):
        # 기본 세팅
        view = UserCodeViewSet()

        rf = APIRequestFactory()
        request = rf.get("/fake-url/")

        users = [
            UserFactory(),
            UserFactory(),
        ]

        for user in users:
            usercodes = UserCodeFactory.create_batch(100, user_id=user)
            request.user = user
            view.request = request
            assert view.get_queryset().count() == len(usercodes)

    def test_usercode_permission(self):
        client = APIClient()

        users = [
            UserFactory(),
            UserFactory(is_staff=True),
            UserFactory(is_superuser=True),
        ]

        UserCodeFactory.create_batch(30, user_id=users[0])
        UserCodeFactory.create_batch(30, user_id=users[1])
        UserCodeFactory.create_batch(30, user_id=users[2])
        usercodes = UserCode.objects.all()

        for user in users:
            client.force_authenticate(user=user)
            for usercode in usercodes:
                usercode_detail_url = reverse(
                    "api:usercode-detail", kwargs={"pk": usercode.pk}
                )
                response = client.get(usercode_detail_url)
                if user == usercode.user:
                    assert response.status_code == status.HTTP_200_OK
                else:
                    assert response.status_code == status.HTTP_404_NOT_FOUND

                response = client.patch(usercode_detail_url, {"code": "Hello world!"})
                if user == usercode.user:
                    assert response.status_code == status.HTTP_200_OK
                else:
                    assert response.status_code == status.HTTP_404_NOT_FOUND
