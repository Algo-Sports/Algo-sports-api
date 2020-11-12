from django.contrib.auth.models import AbstractUser
from django.db.models import AutoField, CharField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for algo_sports."""

    user_id = AutoField(primary_key=True)
    name = CharField(_("Name of User"), blank=True, max_length=255)
    language = CharField(_("Language of User"), blank=True, max_length=30)

    @property
    def id(self):
        return self.user_id
