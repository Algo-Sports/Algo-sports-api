from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for algo_sports."""

    name = CharField(_("Name of User"), blank=True, max_length=255)
    language = CharField(_("Language of User"), blank=True, max_length=30)
