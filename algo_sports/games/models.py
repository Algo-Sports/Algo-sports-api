from typing import Union

from django.db import models
from django.db.models.enums import TextChoices
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from .choices import GameStatus, GameType


class GameVersionType(TextChoices):
    major = "major"
    minor = "minor"
    micro = "micro"


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
        return version.update_change_log(change_log)


class GameVersion(models.Model):
    gameinfo_id = models.ForeignKey(
        GameInfo,
        verbose_name=_("Game information"),
        on_delete=models.PROTECT,
        related_name="versions",
    )

    version = models.JSONField(_("Game Version"), default=make_version)
    change_log = models.JSONField(_("Version change log"), default=dict)
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

    @property
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

    status = models.CharField(
        _("Game status"),
        max_length=2,
        choices=GameStatus.choices,
        default=GameStatus.NOT_STARTED,
    )

    setting = models.JSONField(
        _("Additional setting for GameRoom"),
        blank=True,
        default=dict,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id}. {self.gameinfo} ({self.status})"

    @property
    @cached_property
    def gameinfo(self):
        return self.gameversion.gameinfo

    @cached_property
    def gameversion(self):
        return self.gameversion_id

    @property
    def participantes(self):
        return self.codes.all()
