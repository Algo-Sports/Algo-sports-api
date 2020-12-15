# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import GameInfo, GameMatch, GameRoom, GameVersion


@admin.register(GameInfo)
class GameInfoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "min_users",
        "max_users",
        "extra_info",
        "created_at",
        "updated_at",
    )
    date_hierarchy = "created_at"


@admin.register(GameVersion)
class GameVersionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "gameinfo_id",
        "version",
        "change_log",
        "default_setting",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "gameinfo_id",
        "is_active",
    )
    date_hierarchy = "created_at"


@admin.register(GameRoom)
class GameRoomAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "gameversion_id",
        "type",
        "extra_setting",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "gameversion_id",
        "type",
    )
    date_hierarchy = "created_at"


@admin.register(GameMatch)
class GameMatchAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "gameroom_id",
        "score",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "gameroom_id",
        "status",
    )
    date_hierarchy = "created_at"
