from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from algo_sports.utils.permissions import IsAdminOrReadOnly

from .models import GameInfo, GameRoom
from .serializers import GameInfoSerializer, GameRoomSerializer

# from django.utils.translation import gettext_lazy as _

User = get_user_model()


class GameInfoViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = GameInfoSerializer
    queryset = GameInfo.objects.all()
    lookup_field = "pk"
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=False, methods=["POST"])
    def register_game(self, request):
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"])
    def update_game(self, request):
        return Response(status=status.HTTP_201_CREATED)


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
