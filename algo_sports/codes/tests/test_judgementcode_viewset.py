import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from algo_sports.codes.tests.factories import (
    JudgementCodeFactory,
    ProgrammingLanguageFactory,
)
from algo_sports.games.tests.factories import GameInfoFactory
from algo_sports.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestJudgementCodeViewSet:
    def test_judgementcode_permission(self):
        client = APIClient()

        users = [
            UserFactory(),
            UserFactory(is_staff=True),
            UserFactory(is_superuser=True),
        ]

        for user in users:
            client.force_authenticate(user=user)
            create_url = reverse("api:judgementcode-list")

            gameinfo = GameInfoFactory()
            language = ProgrammingLanguageFactory()

            response = client.post(
                create_url,
                {
                    "gameinfo_id": gameinfo.id,
                    "programming_language": language.pk,
                    "code": "adfsadfasdf",
                },
            )
            if user.is_superuser or user.is_staff:
                assert response.status_code == status.HTTP_201_CREATED
            else:
                assert response.status_code == status.HTTP_403_FORBIDDEN

            judgementcode = JudgementCodeFactory()

            detail_url = reverse(
                "api:judgementcode-detail", kwargs={"pk": judgementcode.pk}
            )
            response = client.get(detail_url, {"code": "Hello world!"})
            if user.is_superuser or user.is_staff:
                assert response.status_code == status.HTTP_200_OK
            else:
                assert response.status_code == status.HTTP_403_FORBIDDEN
