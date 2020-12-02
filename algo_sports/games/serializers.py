from rest_framework import serializers

from .models import GameInfo, GameRoom, GameVersion, GameVersionType


class GameVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameVersion
        exclude = ["change_log"]


class GameInfoSerializer(serializers.ModelSerializer):
    latest_version = serializers.SerializerMethodField(method_name="_version")

    class Meta:
        model = GameInfo
        fields = "__all__"

    def _version(self, instance):
        version = instance.latest_version.version_str
        return version


class GameInfoDetailSerializer(serializers.ModelSerializer):
    change_log = serializers.JSONField()
    version = serializers.SerializerMethodField(method_name="_version")

    class Meta:
        model = GameInfo
        fields = "__all__"

    def _version(self, instance):
        version = instance.latest_version
        print(version)
        return GameVersionSerializer(instance=version).data


class GameInfoUpdateSerializer(serializers.ModelSerializer):
    update_type = serializers.ChoiceField(
        choices=GameVersionType.choices, required=False
    )
    change_log = serializers.ListField(required=False)

    class Meta:
        model = GameInfo
        fields = "__all__"
        read_only_fields = ["title", "description"]

    def validate(self, attrs):
        if attrs["max_users"] > attrs["min_users"]:
            raise serializers.ValidationError("max_users가 min_users 보다 작습니다.")
        return attrs


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
