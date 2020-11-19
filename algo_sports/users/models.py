from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _

from algo_sports.utils.choices import PermissionChoices


class User(AbstractUser):
    """Default user for algo_sports."""

    name = CharField(_("Name of User"), blank=True, max_length=255)
    language = CharField(_("Language of User"), blank=True, max_length=30)

    @property
    def level(self):
        user_level = 1
        if self.is_superuser:
            user_level = PermissionChoices.ADMIN.value
        elif self.is_staff:
            user_level = PermissionChoices.STAFF.value
        return user_level
