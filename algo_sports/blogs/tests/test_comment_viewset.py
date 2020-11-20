import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory

from algo_sports.blogs.tests.factories import CommentFactory, PostFactory
from algo_sports.blogs.views import CommentViewSet
from algo_sports.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestCommentViewSet:
    def test_get_querset(self):
        view = CommentViewSet()

        user = UserFactory()

        rf = APIRequestFactory()
        request = rf.get("/fake_url/")
        request.user = user

        view.request = request

        post = PostFactory()
        parent_size = 10
        CommentFactory.create_batch(parent_size, post_id=post)
        assert view.get_queryset().count() == parent_size

    def test_add_recomment(self):
        client = APIClient()

        user = UserFactory()

        client.force_authenticate(user=user)
        comment = CommentFactory(user_id=user)

        url = reverse("api:comment-add-recomment", kwargs={"pk": comment.pk})
        response = client.post(url, data={"content": "Hello! This is Comment"})

        assert response.status_code == status.HTTP_201_CREATED

        recomment = response.json()
        recomment_pk = recomment.get("id")

        url = reverse("api:comment-add-recomment", kwargs={"pk": recomment_pk})
        response = client.post(url, data={"content": "RereComment is not allowed!"})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_comment_delete(self):
        client = APIClient()

        user = UserFactory()

        client.force_authenticate(user=user)
        comment = CommentFactory(user_id=user)

        url = reverse("api:comment-detail", kwargs={"pk": comment.pk})
        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_deleted_comment_permission(self):
        client = APIClient()

        user = UserFactory()

        client.force_authenticate(user=user)
        comment = CommentFactory(user_id=user)

        url = reverse("api:comment-detail", kwargs={"pk": comment.pk})

        # Delete
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # 삭제 후 수정, 삭제 불가
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

        response = client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = client.put(url, {"content": "Are you deleted?"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = client.patch(url, {"content": "Are you deleted?"})
        assert response.status_code == status.HTTP_403_FORBIDDEN
