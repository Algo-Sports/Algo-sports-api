# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import GameInfo, GameRoom, GameVersion


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
        "status",
        "setting",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "gameversion_id",
        "type",
        "status",
    )
    date_hierarchy = "created_at"
