from django.contrib.auth import get_user_model
from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _

from algo_sports.games.models import GameInfo, GameRoom

User = get_user_model()


class UserCode(models.Model):
    """Code as User"""

    usercode_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    programming_language = models.CharField(_("Programming language"), max_length=30)
    code = models.TextField(_("Submitted code"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def id(self):
        return self.usercode_id

    @property
    def user(self):
        return self.user_id


class JudgementCode(models.Model):
    """Code as Judger"""

    judgementcode_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    gameinfo_id = models.ForeignKey(
        GameInfo,
        verbose_name="Game information",
        on_delete=models.PROTECT,
        related_name="judgement_codes",
    )

    programming_language = models.CharField(_("Programming language"), max_length=30)
    code = models.TextField(_("Submitted code"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def id(self):
        return self.judgementcode_id

    @property
    def user(self):
        return self.gameinfo_id

    @property
    def gameinfo(self):
        return self.gameinfo_id


class GameCodes(models.Model):
    """ManyToMany Through Model for GameInfo and UserCode"""

    gamecodes_id = models.AutoField(primary_key=True)
    usercode_id = models.ForeignKey(UserCode, on_delete=models.PROTECT)
    gameroom_id = models.ForeignKey(GameRoom, on_delete=models.PROTECT)

    score = models.IntegerField(_("Game score"))
    history = JSONField(_("Game history"))

    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    @property
    def id(self):
        return self.gamecodes_id

    @property
    def usercode(self):
        return self.usercode_id

    @property
    def gameroom(self):
        return self.gameroom_id
