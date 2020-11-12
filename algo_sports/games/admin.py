from django.contrib import admin

from .models import GameInfo, GameRoom


@admin.register(GameInfo)
class GameInfoAdmin(admin.ModelAdmin):
    model = GameInfo

    list_display = [
        "title",
        "version",
        "min_users",
        "max_users",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "title",
    ]
    list_filter = [
        "title",
        "min_users",
        "max_users",
    ]


@admin.register(GameRoom)
class GameRoomAdmin(admin.ModelAdmin):
    model = GameRoom

    list_display = [
        "id",
        "gameinfo",
        "status",
        "created_at",
        "finished_at",
    ]
    search_fields = []
    list_filter = [
        "status",
    ]
