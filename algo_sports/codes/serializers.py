from rest_framework import serializers

from algo_sports.users.serializers import UsernameSerializer

from .models import JudgementCode, MatchCodeRelation, ProgrammingLanguage, UserCode


class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingLanguage
        exclude = ["compile_cmd", "run_cmd", "template_code"]


class ProgrammingLanugaeTemplateSerializer(serializers.Serializer):
    parameters = serializers.ListField(
        child=serializers.CharField(required=False),
        write_only=True,
        required=False,
    )
    template_code = serializers.CharField(read_only=True)


class UserCodeSerializer(serializers.ModelSerializer):
    user = UsernameSerializer(source="user_id", read_only=True)

    class Meta:
        model = UserCode
        exclude = ["user_id"]
        read_only_fields = ["is_active"]


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
