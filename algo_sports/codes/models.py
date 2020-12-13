from django.contrib.auth import get_user_model
from django.db import models
from django.template.base import Template
from django.template.context import Context
from django.utils.translation import gettext_lazy as _

from algo_sports.games.models import GameMatch, GameRoom, GameVersion

User = get_user_model()


def make_template_code(main="", solution=""):
    return {"main": main, "solution": solution}


class ProgrammingLanguage(models.Model):
    name = models.CharField(_("Programming language"), max_length=50, unique=True)
    is_active = models.BooleanField(default=False)

    compile_cmd = models.CharField(null=True, blank=True, max_length=500)
    run_cmd = models.CharField(null=True, blank=True, max_length=500)

    template_code = models.JSONField(default=make_template_code)
    extension = models.CharField(_("Language extension"), max_length=10)

    def __str__(self) -> str:
        return f"{self.name}"

    @classmethod
    def active_languages(cls):
        return cls.objects.filter(is_active=True)

    def get_solution_template(self, parameters: list([str])):
        parameters = ", ".join(parameters)

        raw_template = self.template_code.get("solution")
        template = Template(raw_template)
        context = Context({"parameters": parameters})
        template_code = template.render(context)
        return template_code

    def get_main_template(
        self, include: list([str]), arguments: list([str]), solution: str
    ):
        includes = "\n".join(include)
        arguments = ", ".join(arguments)

        raw_template = self.template_code.get("main")
        template = Template(raw_template)
        context = Context(
            {"includes": includes, "arguments": arguments, "solution": solution}
        )
        template_code = template.render(context)
        return template_code


class UserCode(models.Model):
    """Code as User"""

    user_id = models.ForeignKey(
        User, related_name="usercodes", blank=True, null=True, on_delete=models.SET_NULL
    )
    gamerooms = models.ForeignKey(
        GameRoom, related_name="usercodes", null=True, on_delete=models.PROTECT
    )
    gamematches = models.ManyToManyField(
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

    user_id = models.ForeignKey(
        User,
        related_name="judgementcodes",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    gameversion_id = models.ForeignKey(
        GameVersion,
        verbose_name=_("Game version"),
        on_delete=models.PROTECT,
        related_name="judgementcodes",
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
