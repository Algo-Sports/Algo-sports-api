from django.db import models
from django.utils.translation import gettext_lazy as _


class GameType(models.TextChoices):
    GENERAL = "GE", _("General")
    PRACTICE = "PR", _("Practice")
    RANKING = "RA", _("Ranking")
    __empty__ = _("(Unknown)")


class GameStatus(models.TextChoices):
    NOT_STARTED = "NS", _("Not started")
    IN_PROGRESS = "IN", _("In progress")
    FINISHED = "FN", _("Finished")
    ERROR_OCCURED = "EO", _("Error occured")
    __empty__ = _("(Unknown)")


class GameVersionType(models.TextChoices):
    major = "major"
    minor = "minor"
    micro = "micro"
