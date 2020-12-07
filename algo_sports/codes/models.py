from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from algo_sports.games.models import GameMatch, GameRoom, GameVersion

User = get_user_model()


class ProgrammingLanguage(models.Model):
    name = models.SlugField(_("Programming language"), max_length=50, unique=True)
    is_active = models.BooleanField(default=False)

    compile_cmd = models.CharField(null=True, blank=True, max_length=500)
    run_cmd = models.CharField(null=True, blank=True, max_length=500)

    def __str__(self) -> str:
        return f"{self.name}"


class UserCode(models.Model):
    """Code as User"""

    user_id = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    gameroom = models.ForeignKey(
        GameRoom, related_name="usercodes", on_delete=models.PROTECT
    )
    gamematchs = models.ManyToManyField(
        GameMatch, related_name="usercodes", through="MatchCodeRelation"
    )

    programming_language = models.ForeignKey(
        ProgrammingLanguage,
        verbose_name=_("Programming language"),
        on_delete=models.PROTECT,
    )
    code = models.TextField(_("Submitted code"))

    is_active = models.BooleanField(_("Is code active?"), default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def user(self):
        return self.user_id


class JudgementCode(models.Model):
    """Code as Judger"""

    user_id = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    gameversion_id = models.ForeignKey(
        GameVersion,
        verbose_name=_("Game version"),
        on_delete=models.PROTECT,
        related_name="judgement_codes",
    )

    programming_language = models.ForeignKey(
        ProgrammingLanguage,
        verbose_name=_("Programming language"),
        on_delete=models.PROTECT,
    )
    code = models.TextField(_("Submitted code"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def user(self):
        return self.gameversion_id

    @property
    def gameversion(self):
        return self.gameversion_id


class MatchCodeRelation(models.Model):
    """ManyToMany Through Model for GameMatch and UserCode"""

    usercode_id = models.ForeignKey(UserCode, on_delete=models.PROTECT)
    gamematch_id = models.ForeignKey(GameMatch, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "match_code_relation"

    @property
    def usercode(self):
        return self.usercode_id

    @property
    def gamematch(self):
        return self.gamematch_id
