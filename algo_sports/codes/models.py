from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from algo_sports.games.models import GameInfo, GameRoom

User = get_user_model()


class UserCode(models.Model):
    """Code as User"""

    user_id = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    gamerooms = models.ManyToManyField(
        GameRoom, related_name="usercodes", through="CodeRoomRelation"
    )

    programming_language = models.CharField(_("Programming language"), max_length=30)
    code = models.TextField(_("Submitted code"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def user(self):
        return self.user_id


class JudgementCode(models.Model):
    """Code as Judger"""

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
    def user(self):
        return self.gameinfo_id

    @property
    def gameinfo(self):
        return self.gameinfo_id


class CodeRoomRelation(models.Model):
    """ManyToMany Through Model for GameInfo and UserCode"""

    usercode_id = models.ForeignKey(UserCode, on_delete=models.PROTECT)
    gameroom_id = models.ForeignKey(GameRoom, on_delete=models.PROTECT)

    score = models.IntegerField(_("Game score"))
    history = models.JSONField(_("Game history"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "code_room_relation"

    @property
    def usercode(self):
        return self.usercode_id

    @property
    def gameroom(self):
        return self.gameroom_id
