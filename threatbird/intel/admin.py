from django.contrib import admin

from .models import Technique, Tactic, APTGroup

# Register your models here.
@admin.register(Technique)
class TechniqueAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "inserted", "name", "url",)
    ordering = ("-id",)


@admin.register(Tactic)
class TacticAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "inserted", "name", "url",)
    ordering = ("-id",)


@admin.register(APTGroup)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "inserted", "name", "aliases",)
    ordering = ("-id",)

