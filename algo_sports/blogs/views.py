from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from algo_sports.blogs.filters import BlogFilter, CommentFilter, PostFilter
from algo_sports.utils.paginations import SizeQueryPagination
from algo_sports.utils.permissions import IsOwnerOrReadOnly, IsSuperUser

from .models import Blog, Comment, Post
from .serializers import (
    BlogSerializer,
    CommentSerializer,
    PostSerializer,
    ReCommentSerializer,
)

User = get_user_model()


class BlogViewSet(
    ListModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    """
    Blog 리스트, 업데이트, 디테일 ViewSet

    @action
    add_post : 해당 블로그에 포스트 생성
    """

    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    lookup_field = "category"
    permission_classes = [IsAuthenticatedOrReadOnly | IsSuperUser]
    filterset_class = BlogFilter

    action_serializer_classes = {
        "add_post": PostSerializer,
    }

    def get_queryset(self):
        queryset = self.queryset.filter(permission__lte=self.request.user.level)
        return queryset

    def get_serializer_class(self):
        serializer = self.action_serializer_classes.get(self.action)
        if serializer:
            return serializer
        return super().get_serializer_class()

    @action(detail=True, methods=["POST"])
    def add_post(self, request, *args, **kwargs):
        blog = self.get_object()
        if blog.permission <= request.user.level:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user_id=request.user, blog_id=blog)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN)


class PostViewSet(
    ListModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    """
    Post 리스트, 업데이트, 디테일 ViewSet

    @action
    add_comment : 해당 포스트에 댓글 생성
    """

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsSuperUser | IsOwnerOrReadOnly]
    lookup_field = "pk"
    pagination_class = SizeQueryPagination
    filterset_class = PostFilter

    action_serializer_classes = {
        "add_comment": CommentSerializer,
    }

    def get_serializer_class(self):
        serializer = self.action_serializer_classes.get(self.action)
        if serializer:
            return serializer
        return super().get_serializer_class()

    @action(detail=True, methods=["POST"])
    def add_comment(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user, post_id=self.get_object())
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewSet(
    ListModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    """
    Comment 조회, 갱신, 삭제

    @action
    add_recomment : 해당 댓글에 대댓글 생성
    """

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsSuperUser | IsOwnerOrReadOnly]
    lookup_field = "pk"
    pagination_class = SizeQueryPagination
    filterset_class = CommentFilter

    action_serializer_classes = {
        "add_recomment": ReCommentSerializer,
    }

    def get_serializer_class(self):
        serializer = self.action_serializer_classes.get(self.action)
        if serializer:
            return serializer
        return super().get_serializer_class()

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.deleted = True
        comment.save()

    @action(detail=True, methods=["POST"])
    def add_recomment(self, request, *args, **kwargs):
        comment = self.get_object()
        # 이미 부모를 가지고 있는 대댓글 같은 경우에는 자식을 가지지 못한다.
        if comment.parent is not None:
            return Response(
                {"detail": "400 BAD REQUEST"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user_id=request.user,
            parent_id=comment,
            post_id=comment.post_id,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
