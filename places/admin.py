from django.contrib.gis import admin

from .models import Place


@admin.register(Place)
class PlaceAdmin(admin.GISModelAdmin):

    list_display = (
        'name',
        'category',
        'is_accessible',
        'updated_at',
    )

    list_filter = (
        'category',
        'is_accessible',
    )

    search_fields = (
        'name',
        'description',
    )