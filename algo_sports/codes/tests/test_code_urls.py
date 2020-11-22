import pytest
from django.urls import resolve, reverse

from algo_sports.codes.tests.factories import UserCodeFactory
from algo_sports.utils.test.compare_url import compare_url

pytestmark = pytest.mark.django_db


def test_usercode_url():
    usercode = UserCodeFactory()
    lookup_field = "pk"
    lookup_value = usercode.pk
    middle_url = "codes/user"

    # reverse url
    assert compare_url(
        reverse("api:usercode-detail", kwargs={lookup_field: lookup_value}),
        f"/api/{middle_url}/{lookup_value}/",
    )
    assert compare_url(reverse("api:usercode-list"), f"/api/{middle_url}/")

    # resolve view name
    assert (
        resolve(f"/api/{middle_url}/{lookup_value}/").view_name == "api:usercode-detail"
    )
    assert resolve(f"/api/{middle_url}/").view_name == "api:usercode-list"


def test_judgementcode_url():
    judgementcode = UserCodeFactory()
    lookup_field = "pk"
    lookup_value = judgementcode.pk
    middle_url = "codes/judegement"

    # reverse url
    assert compare_url(
        reverse("api:judgementcode-detail", kwargs={lookup_field: lookup_value}),
        f"/api/{middle_url}/{lookup_value}/",
    )
    assert compare_url(reverse("api:judgementcode-list"), f"/api/{middle_url}/")

    # resolve view name
    assert (
        resolve(f"/api/{middle_url}/{lookup_value}/").view_name
        == "api:judgementcode-detail"
    )

    assert resolve(f"/api/{middle_url}/").view_name == "api:judgementcode-list"
