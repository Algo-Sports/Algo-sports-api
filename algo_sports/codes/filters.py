from django_filters import rest_framework as filters
from django_filters.filters import CharFilter

from .models import JudgementCode, UserCode


class UserCodeFilter(filters.FilterSet):
    user = CharFilter(field_name="user_id__username")

    class Meta:
        model = UserCode
        fields = (
            "user",
            "programming_language",
        )


class JudgementCodeFilter(filters.FilterSet):
    user = CharFilter(field_name="user_id__username")

    class Meta:
        model = JudgementCode
        fields = (
            "user",
            "gameinfo_id",
            "programming_language",
        )
