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

    gameinfo_id = models.ForeignKey(
        GameInfo,
        verbose_name="Game information",
        on_delete=models.PROTECT,
        related_name="game_rooms",
    )
    status = models.PositiveSmallIntegerField(_("Game status"), default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.id}. {self.gameinfo} ({self.status})"

    @property
    def gameinfo(self):
        return self.gameinfo_id
