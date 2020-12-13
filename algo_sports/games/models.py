from typing import Union

import numpy
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.http import Http404
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from .choices import GameStatus, GameType, GameVersionType

User = get_user_model()


def make_version(major=0, minor=0, micro=1):
    return {
        GameVersionType.major: major,
        GameVersionType.minor: minor,
        GameVersionType.micro: micro,
    }


class GameInfo(models.Model):
    """Information of Game"""

    title = models.CharField(_("Game title"), max_length=50, unique=True)
    description = models.TextField(_("Game describtion"))

    min_users = models.PositiveSmallIntegerField(_("Minimum User number"))
    max_users = models.PositiveSmallIntegerField(_("Maximum User number"))

    extra_info = models.JSONField(_("Additional information of Game"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return f"{self.title} ({self.total_versions})"

    def get_version(self, version: dict):
        filtered = self.get_versions().filter(version=version)
        if not filtered.exists():
            return Http404()
        return filtered[0]

    def get_versions(self, ordering=False):
        versions = self.versions.all()
        if ordering:
            versions = versions.order_by(
                "-version__major",
                "-version__minor",
                "-version__micro",
            )
        return versions

    @property
    def is_active(self):
        return self.total_versions > 0

    @property
    def change_log(self):
        return self.get_versions(ordering=True).values_list("version", "change_log")

    @property
    def latest_version(self):
        return self.get_versions(ordering=True).first()

    @property
    def total_versions(self):
        return self.versions.all().count()

    def update_version(
        self,
        update_type: GameVersionType,
        change_log: Union[str, list],
        default_setting: dict = None,
        target_version: dict = None,
    ):
        if not self.is_active:
            # 게임 정보만 존재할 시 새로 버전을 생성
            GameVersion.objects.create(gameinfo_id=self, version=make_version(0, 0, 0))

        version = None
        if target_version:
            version.get_versions(ordering=True).filter(version=target_version).first()
        else:
            version = self.latest_version

        if update_type == GameVersionType.major:
            version = version.major_up()
        elif update_type == GameVersionType.minor:
            version = version.minor_up()
        elif update_type == GameVersionType.micro:
            version = version.micro_up()
        else:
            raise "Unexpected update type"

        if default_setting:
            version.default_setting = default_setting
            version.save()
        return version.update_change_log(change_log)


def get_default_setting():
    return {
        "includes": {
            "Python (3.8.1)": [],
        },
        "arguments": {
            "Python (3.8.1)": ["argv[0]"],
        },
        "parameters": {
            "Python (3.8.1)": ["greeting: str"],
        },
    }


class GameVersion(models.Model):
    gameinfo_id = models.ForeignKey(
        GameInfo,
        verbose_name=_("Game information"),
        on_delete=models.PROTECT,
        related_name="versions",
    )

    version = models.JSONField(_("Game Version"), default=make_version)
    change_log = models.JSONField(_("Version change log"), default=dict)
    default_setting = models.JSONField(
        _("Version default setting"), default=get_default_setting
    )
    is_active = models.BooleanField(_("Is this version active?"), default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.gameinfo.title} ({self.version_str})"

    class Meta:
        unique_together = ["gameinfo_id", "version"]
        ordering = [
            "version__micro",
            "version__minor",
            "version__major",
        ]

    @cached_property
    def gameinfo(self):
        return self.gameinfo_id

    @property
    def version_str(self):
        version = f"v{self.version[GameVersionType.major]}."
        version += f"{self.version[GameVersionType.minor]}."
        version += f"{self.version[GameVersionType.micro]}"
        return version

    def major_up(self):
        self.pk = None
        self.version[GameVersionType.major] += 1
        self.version[GameVersionType.minor] = 0
        self.version[GameVersionType.micro] = 0
        self.change_log = {}
        self.save()
        return self

    def minor_up(self):
        self.version[GameVersionType.minor] += 1
        self.version[GameVersionType.micro] = 0
        self.save()
        return self

    def micro_up(self):
        self.version[GameVersionType.micro] += 1
        self.save()
        return self

    def update_change_log(self, changes: Union[str, list]):
        self.change_log.setdefault(self.version_str, [])
        if isinstance(changes, str):
            self.change_log.get(self.version_str).append(changes)
        else:
            self.change_log.get(self.version_str).extend(changes)
        self.save()
        return self


class GameRoom(models.Model):
    """Room for storing game status"""

    gameversion_id = models.ForeignKey(
        GameVersion,
        verbose_name=_("Game Version"),
        on_delete=models.PROTECT,
        related_name="game_rooms",
    )

    type = models.CharField(
        _("Game Type"),
        max_length=2,
        choices=GameType.choices,
        default=GameType.GENERAL,
    )

    extra_setting = models.JSONField(
        _("Additional setting for GameRoom"),
        blank=True,
        default=dict,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Room {self.id}. {self.gameversion} ({self.type})"

    @property
    def is_active(self):
        min_user = self.gameinfo.min_users
        return self.active_participants.count() > min_user

    @cached_property
    def gameinfo(self):
        return self.gameversion.gameinfo

    @cached_property
    def gameversion(self):
        return self.gameversion_id

    @property
    def participants(self):
        return self.usercodes.all()

    @property
    def active_participants(self):
        return self.participants.select_related("programming_language").filter(
            programming_language__is_active=True, is_active=True
        )

    def sample_active_participants(self, exclude_user) -> list([int]):
        if not self.is_active:
            return []

        # 자신을 제외한 유저코드 추출
        queryset = self.active_participants.filter(
            ~Q(user_id=exclude_user)
        ).values_list("id", flat=True)
        actives = queryset.count()

        # 매치를 시작할 유저를 제외한 수
        max_users = self.gameinfo.max_users - 1
        min_users = self.gameinfo.min_users - 1

        sample_size = 0
        if actives > 0 and actives < max_users:
            sample_size = min_users
        elif actives >= max_users:
            sample_size = max_users

        sampled = numpy.array([])
        if sample_size > 0:
            sampled = numpy.random.choice(queryset, size=sample_size, replace=False)

        # 균일 추출, 동일값 없음.
        return sampled.tolist()


class GameMatch(models.Model):
    """Match in Game room"""

    gameroom_id = models.ForeignKey(
        GameRoom,
        verbose_name=_("Game room"),
        on_delete=models.PROTECT,
        related_name="game_matchs",
    )

    history = models.JSONField(
        _("History in Game Match"),
        blank=True,
        default=dict,
    )

    score = models.IntegerField(_("Match Score"), blank=True, default=0)

    status = models.CharField(
        _("Game Match Status"),
        max_length=2,
        choices=GameStatus.choices,
        default=GameStatus.NOT_STARTED,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id}. ({self.status})"

    def set_status(self, status: GameStatus):
        self.status = status
        self.save()
