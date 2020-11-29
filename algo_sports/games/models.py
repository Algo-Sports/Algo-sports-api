from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import GameStatus, GameType


class GameVersionType(str, Enum):
    major = "major"
    minor = "minor"
    micro = "micro"


def get_default_version():
    return {
        GameVersionType.major: 0,
        GameVersionType.minor: 0,
        GameVersionType.micro: 1,
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

    @property
    def is_active(self):
        return self.total_versions > 0

    @property
    def change_log(self):
        return self.versions.all().values_list("change_log")

    @property
    def latest_version(self):
        return (
            self.versions.all()
            .order_by(
                "-version__major",
                "-version__minor",
                "-version__micro",
            )
            .first()
        )

    @property
    def total_versions(self):
        return self.versions.all().count()


class GameVersion(models.Model):
    gameinfo_id = models.ForeignKey(
        GameInfo,
        verbose_name=_("Game information"),
        on_delete=models.PROTECT,
        related_name="versions",
    )

    version = models.JSONField(_("Game Version"), default=get_default_version)
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
        self.version[GameVersionType.major] += 1
        self.version[GameVersionType.minor] = 0
        self.version[GameVersionType.micro] = 0
        self.save()

    def minor_up(self):
        self.version[GameVersionType.minor] += 1
        self.version[GameVersionType.micro] = 0
        self.save()

    def micro_up(self):
        self.version[GameVersionType.micro] += 1
        self.save()


class GameRoom(models.Model):
    """Room for storing game status"""

    gameinfo_id = models.ForeignKey(
        GameInfo,
        verbose_name=_("Game information"),
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
    def gameinfo(self):
        return self.gameinfo_id

    @property
    def participantes(self):
        return self.codes.all()
