from django_filters import rest_framework as filters
from django_filters.filters import CharFilter

from .models import JudgementCode, UserCode


class UserCodeFilter(filters.FilterSet):
    user = CharFilter(field_name="user_id__username")

    class Meta:
        model = UserCode
        fields = (
            "is_active",
            "programming_language",
            "gamerooms",
        )


class JudgementCodeFilter(filters.FilterSet):
    user = CharFilter(field_name="user_id__username")

    class Meta:
        model = JudgementCode
        fields = (
            "user",
            "gameversion_id",
            "programming_language",
        )
