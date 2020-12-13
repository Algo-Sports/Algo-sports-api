from rest_framework import serializers

from .models import GameInfo, GameRoom


class GameInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameInfo
        fields = [
            "title",
            "version",
            "description",
            "min_users",
            "max_users",
            "extra_info",
            "created_at",
            "updated_at",
        ]


class GameRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRoom
        fields = [
            "gameinfo",
            "type",
            "status",
            "setting",
            "created_at",
            "updated_at",
        ]
