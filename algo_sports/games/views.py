from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from algo_sports.utils.permissions import IsAdminOrReadOnly

from .models import GameInfo, GameRoom, GameVersionType
from .serializers import (
    GameInfoDetailSerializer,
    GameInfoSerializer,
    GameInfoUpdateSerializer,
    GameRoomSerializer,
)

# from django.utils.translation import gettext_lazy as _

User = get_user_model()


class GameInfoViewSet(
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = GameInfoSerializer
    queryset = GameInfo.objects.all()
    lookup_field = "pk"
    permission_classes = [IsAdminOrReadOnly]

    action_serializer_classes = {
        "retrieve": GameInfoDetailSerializer,
        "update": GameInfoUpdateSerializer,
        "partial_update": GameInfoUpdateSerializer,
    }

    def get_serializer_class(self):
        serializer = self.action_serializer_classes.get(self.action)
        if serializer:
            return serializer
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        """
        GameInfo의 Version을 한 단계 올린다.
        """
        gameinfo = self.get_object()
        update_type = request.data.get("update_type", GameVersionType.micro)
        change_log = request.data.get("change_log")

        request.data.pop("update_type")
        request.data.pop("change_log")

        if change_log:
            gameinfo.update_version(
                update_type=update_type,
                change_log=change_log,
            )
            return super().update(request, *args, **kwargs)

        return Response(
            data={"detail": "Change log is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True, methods=["GET"])
    def get_active_versions(self, request):
        queryset = self.queryset.get_versions(ordering=True)
        queryset = queryset.filter(is_active=True)
        return Response(status=status.HTTP_200_OK)


class GameRoomViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = GameRoomSerializer
    queryset = GameRoom.objects.all()
    lookup_field = "pk"

    @action(detail=True, methods=["GET"])
    def get_joined_codes(self, request):
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"])
    def join_room(self, request):
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def make_room(self, request):
        return Response(status=status.HTTP_200_OK)
