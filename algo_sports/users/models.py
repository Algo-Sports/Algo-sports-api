from django.contrib.auth.models import AbstractUser
from django.db.models import AutoField, CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for algo_sports."""

    user_id = AutoField(primary_key=True)
    name = CharField(_("Name of User"), blank=True, max_length=255)
    language = CharField(_("Language of User"), blank=True, max_length=30)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
