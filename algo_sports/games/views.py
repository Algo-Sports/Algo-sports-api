from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
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

from .models import GameInfo, GameMatch, GameRoom, GameVersion, GameVersionType
from .serializers import (
    GameInfoDetailSerializer,
    GameInfoSerializer,
    GameInfoUpdateSerializer,
    GameMatchSerializer,
    GameRoomCreateSerializer,
    GameRoomSerializer,
)
from .tasks import run_match

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
        "create_gameroom": GameRoomCreateSerializer,
    }

    def get_serializer_class(self):
        serializer = self.action_serializer_classes.get(self.action)
        if serializer:
            return serializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        """
        GameInfo 생성할 때 Version을 하나 생성한다.
        """
        version_args = {}

        default_setting = request.data.get("default_setting")
        if default_setting:
            request.data.pop("default_setting")
            version_args["default_setting"] = default_setting

        response = super().create(request, *args, **kwargs)
        gameinfo = GameInfo.objects.get(id=response.data.get("id"))
        version_args["gameinfo_id"] = gameinfo

        GameVersion.objects.create(**version_args)

        serializer = self.get_serializer(instance=gameinfo)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        """
        GameInfo의 Version을 한 단계 올린다.
        """
        gameinfo = self.get_object()

        update_type = request.data.get("update_type")
        if update_type:
            request.data.pop("update_type")
            update_type = GameVersionType.micro

        default_setting = request.data.get("default_setting")
        if default_setting:
            request.data.pop("default_setting")

        change_log = request.data.get("change_log")
        if change_log:
            request.data.pop("change_log")

        if change_log:
            if default_setting:
                gameinfo.update_version(
                    update_type=update_type,
                    change_log=change_log,
                    default_setting=default_setting,
                )
            else:
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

    @action(detail=True, methods=["POST"])
    def create_gameroom(self, request, *args, **kwargs):
        gameinfo = self.get_object()

        version = request.data.get("version")

        gameversion_id = None
        if version:
            gameversion_id = gameinfo.get_version(version=version)
            request.data.pop("version")
        else:
            gameversion_id = gameinfo.latest_version

        serializers = self.get_serializer(data=request.data)
        serializers.is_valid()
        serializers.save(gameversion_id=gameversion_id)

        return Response(data=serializers.data, status=status.HTTP_201_CREATED)


class GameRoomViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = GameRoomSerializer
    queryset = GameRoom.objects.all()
    lookup_field = "pk"

    action_serializer_classes = {}

    def get_serializer_class(self):
        serializer = self.action_serializer_classes.get(self.action)
        if serializer:
            return serializer
        return super().get_serializer_class()

    @action(detail=True, methods=["GET"])
    def total_participants(self, request):
        """ The number of joined users """
        gameroom = self.get_object()
        num_participants = gameroom.participants.count()
        num_active_participants = gameroom.active_participants.count()
        data = {
            "num_participants": num_participants,
            "num_active_participants": num_active_participants,
        }
        return Response(data=data, status=status.HTTP_200_OK)


class GameMatchViewSet(
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet
):
    serializer_class = GameMatchSerializer
    queryset = GameMatch.objects.all()

    action_serializer_classes = {}

    def get_serializer_class(self):
        serializer = self.action_serializer_classes.get(self.action)
        if serializer:
            return serializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        """ Create match """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 경쟁 코드들
        gameroom = get_object_or_404(GameRoom, pk=serializer.data.get("gameroom_id"))
        competitor_ids = gameroom.sample_active_participants(
            exclude_user=self.request.user
        )

        if len(competitor_ids) == 0:
            return Response(
                data={"msg": _("참가자들이 부족합니다.")}, status=status.HTTP_400_BAD_REQUEST
            )

        # 참가할 매치
        gamematch = get_object_or_404(GameMatch, pk=serializer.data.get("id"))
        gamematch.usercodes.add(*competitor_ids)

        # celery task 실행
        run_match.delay(
            {
                "gameroom_id": gameroom.id,
                "gamematch_id": gamematch.id,
                "competitor_ids": competitor_ids.tolist(),
            }
        )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
