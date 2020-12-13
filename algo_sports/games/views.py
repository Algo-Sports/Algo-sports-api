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


def make_run_match_parameter(
    gameroom_id: int,
    gamematch_id: int,
    competitor_ids: list([int]),
):
    return {
        "gameroom_id": gameroom_id,
        "gamematch_id": gamematch_id,
        "competitor_ids": competitor_ids,
    }


class GameMatchViewSet(
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet
):
    serializer_class = GameMatchSerializer
    queryset = GameMatch.objects.all()

    action_serializer_classes = {}

    def get_queryset(self):
        gamematche_ids = self.request.user.usercodes.values_list(
            "gamematches", flat=True
        )
        return GameMatch.objects.filter(id__in=gamematche_ids)

    def get_serializer_class(self):
        serializer = self.action_serializer_classes.get(self.action)
        if serializer:
            return serializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        """ Create match """
        # match에 직접적으로 저장되지 않는 데이터 추출
        mycode_id = request.data.get("mycode_id")
        if mycode_id:
            request.data.pop("mycode_id")

        # 저장은 안하고 유효한 입력인지 확인 진행
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # gameroom object
        gameroom = serializer.validated_data.get("gameroom_id")

        # mycode object
        mycode_obj = gameroom.participants.filter(pk=mycode_id)
        if not mycode_obj.exists():
            # 방에 참가한 코드인지 확인
            return Response(
                data={"msg": _("현재 방에 참가하지 않은 코드입니다.")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif not mycode_obj[0].user.id == request.user.id:
            # 현재 로그인한 유저의 코드인지 확인
            return Response(
                data={"msg": _("소유하지 않은 코드입니다.")},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 경쟁 코드들 샘플링
        competitor_ids = gameroom.sample_active_participants(
            exclude_user=self.request.user
        )

        # 참가자가 충분한지 확인
        if len(competitor_ids) == 0:
            return Response(
                data={"msg": _("참가자들이 부족합니다.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 매치를 만드는 사용자의 코드를 0번 인덱스에 추가
        competitor_ids.insert(0, mycode_id)

        # 유효한 입력이므로 Match 생성
        serializer.save()

        # 참가할 매치
        gamematch = get_object_or_404(GameMatch, pk=serializer.data.get("id"))
        gamematch.usercodes.add(*competitor_ids)

        # celery task 실행
        run_match.delay(
            make_run_match_parameter(
                gameroom.id,
                gamematch.id,
                competitor_ids,
            )
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
