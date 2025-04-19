from django.contrib import admin
from .models import Dragon, Race

admin.site.register(Dragon)

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ("name", "base_res", "base_vit", "base_dre", "base_gal", "base_sar", "base_tra")