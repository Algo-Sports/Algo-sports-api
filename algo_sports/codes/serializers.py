from rest_framework import serializers

from algo_sports.users.serializers import UsernameSerializer

from .models import JudgementCode, MatchCodeRelation, UserCode


class UserCodeSerializer(serializers.ModelSerializer):
    user = UsernameSerializer(read_only=True)

    class Meta:
        model = UserCode
        fields = "__all__"


class JudgementCodeSerializer(serializers.ModelSerializer):
    user = UsernameSerializer(source="user_id", read_only=True)

    class Meta:
        model = JudgementCode
        fields = [
            "id",
            "user",
            "gameinfo_id",
            "programming_language",
            "code",
            "created_at",
            "updated_at",
        ]


class MatchCodeRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchCodeRelation
        fields = [
            "id",
            "usercode",
            "gamematch",
            "created_at",
            "updated_at",
        ]
