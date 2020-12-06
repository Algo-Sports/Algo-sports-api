from rest_framework import serializers

from algo_sports.users.serializers import UsernameSerializer

from .models import JudgementCode, MatchCodeRelation, UserCode


class UserCodeSerializer(serializers.ModelSerializer):
    user = UsernameSerializer(read_only=True)

    class Meta:
        model = UserCode
        exclude = ["user_id"]


class JudgementCodeSerializer(serializers.ModelSerializer):
    user = UsernameSerializer(source="user_id", read_only=True)

    class Meta:
        model = JudgementCode
        exclude = ["user_id"]


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
