from django.db.models import IntegerChoices


class PermissionChoices(IntegerChoices):
    ADMIN = 3, "Admin only"
    STAFF = 2, "Staff only"
    ALL = 1, "Allow any"
