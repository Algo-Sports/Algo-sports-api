from django.contrib import admin

from .models import CodeRoomRelation, JudgementCode, ProgrammingLanguage, UserCode


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(UserCode)
class UserCodeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "programming_language",
        "code",
        "created_at",
        "updated_at",
    )
    list_filter = ("user_id", "programming_language", "created_at", "updated_at")
    search_fields = ["author"]
    raw_id_fields = ("gamerooms",)
    date_hierarchy = "created_at"

    def author(self, obj):
        return obj.user.username


@admin.register(JudgementCode)
class JudgementCodeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "gameinfo_id",
        "programming_language",
        "code",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "user_id",
        "gameinfo_id",
        "programming_language",
        "created_at",
        "updated_at",
    )
    search_fields = ("author", "gameinfo__title")
    date_hierarchy = "created_at"

    def author(self, obj):
        return obj.user.username


@admin.register(CodeRoomRelation)
class CodeRoomRelationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usercode_id",
        "gameroom_id",
        "score",
        "history",
        "created_at",
        "updated_at",
    )
    list_filter = ("usercode_id", "gameroom_id", "created_at", "updated_at")
    date_hierarchy = "created_at"
