from django_filters import rest_framework as filters

from .models import GameMatch


class GameMatchFilter(filters.FilterSet):
    class Meta:
        model = GameMatch
        fields = ("gameroom_id",)
