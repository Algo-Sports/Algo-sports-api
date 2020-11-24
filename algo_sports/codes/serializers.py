from rest_framework import serializers

from algo_sports.users.serializers import UsernameSerializer

from .models import CodeRoomRelation, JudgementCode, UserCode


class UserCodeSerializer(serializers.ModelSerializer):
    user = UsernameSerializer(read_only=True)

    class Meta:
        model = UserCode
        fields = [
            "user",
            "programming_language",
            "code",
            "created_at",
            "updated_at",
        ]


class JudgementCodeSerializer(serializers.ModelSerializer):
    user = UsernameSerializer(source="user_id", read_only=True)

    class Meta:
        model = JudgementCode
        fields = [
            "user",
            "gameinfo_id",
            "programming_language",
            "code",
            "created_at",
            "updated_at",
        ]


class CodeRoomRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeRoomRelation
        fields = [
            "usercode",
            "gameroom",
            "score",
            "history",
            "created_at",
            "updated_at",
        ]
