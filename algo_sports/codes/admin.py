from django.contrib import admin

from .models import JudgementCode, UserCode


@admin.register(UserCode)
class UserCodeAdmin(admin.ModelAdmin):
    model = UserCode

    list_display = [
        "id",
        "author",
        "programming_language",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "author",
    ]
    list_filter = [
        "programming_language",
    ]

    def author(self, obj):
        return obj.user.username


@admin.register(JudgementCode)
class JudgementCodeAdmin(admin.ModelAdmin):
    model = JudgementCode

    list_display = [
        "id",
        "author",
        "gameinfo",
        "programming_language",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "author",
        "gameinfo__title",
    ]
    list_filter = [
        "programming_language",
    ]

    def author(self, obj):
        return obj.user.username
