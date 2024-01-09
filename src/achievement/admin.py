from django.contrib import admin

from .models import Olympiad


@admin.register(Olympiad)
class OlympiadAdmin(admin.ModelAdmin):
    pass
