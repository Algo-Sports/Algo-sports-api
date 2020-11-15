from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _


class GameInfo(models.Model):
    """Information of Game"""

    title = models.CharField(_("Game title"), max_length=50)
    version = models.CharField(_("Game Version"), max_length=10)
    description = models.TextField(_("Game describtion"))

    min_users = models.PositiveSmallIntegerField(_("Minimum User number"))
    max_users = models.PositiveSmallIntegerField(_("Maximum User number"))

    extra_info = JSONField(_("Additional information of Game"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.title} - v{self.version}"


class GameRoom(models.Model):
    """Room for storing game status"""

    class GameType(models.TextChoices):
        GENERAL = "GE", _("General")
        PRACTICE = "PR", _("Practice")
        RANKING = "RA", _("Ranking")

    class GameStatus(models.TextChoices):
        NOT_STARTED = "NS", _("Not started")
        FINISHED = "FN", _("Finished")
        ERROR_OCCURED = "EO", _("Error occured")

    gameinfo_id = models.ForeignKey(
        GameInfo,
        verbose_name="Game information",
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

    setting = JSONField(
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
