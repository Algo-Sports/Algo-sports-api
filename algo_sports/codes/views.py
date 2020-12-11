from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from algo_sports.codes.filters import JudgementCodeFilter, UserCodeFilter
from algo_sports.utils.permissions import (
    IsAdminUser,
    IsOwnerOrReadAndPostOnly,
    IsSuperUser,
)

from .models import JudgementCode, UserCode
from .serializers import JudgementCodeSerializer, UserCodeSerializer

# from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserCodeViewSet(ModelViewSet):
    """
    UserCode 리스트, 업데이트, 디테일 ViewSet
    """

    serializer_class = UserCodeSerializer
    queryset = UserCode.objects.all()
    lookup_field = "pk"
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadAndPostOnly | IsSuperUser,
    ]
    filterset_class = UserCodeFilter

    action_serializer_classes = {}

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user)

    def get_serializer_class(self):
        serializer = self.action_serializer_classes.get(self.action)
        if serializer:
            return serializer

        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class JudgementCodeViewSet(ModelViewSet):
    """
    JudegementCode 리스트, 업데이트, 디테일 ViewSet
    """

    serializer_class = JudgementCodeSerializer
    queryset = JudgementCode.objects.all()
    lookup_field = "pk"
    permission_classes = [IsAdminUser]
    filterset_class = JudgementCodeFilter

    action_serializer_classes = {}

    def get_serializer_class(self):
        serializer = self.action_serializer_classes.get(self.action)
        if serializer:
            return serializer

        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
