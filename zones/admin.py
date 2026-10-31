from django.contrib.gis import admin

from .models import Zone


@admin.register(Zone)
class ZoneAdmin(admin.GISModelAdmin):

    list_display = (
        'name',
        'zone_type',
        'updated_at',
    )

    list_filter = (
        'zone_type',
    )

    search_fields = (
        'name',
        'description',
    )