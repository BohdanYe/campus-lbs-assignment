from django.contrib.gis import admin

from .models import Route


@admin.register(Route)
class RouteAdmin(admin.GISModelAdmin):

    list_display = (
        'name',
        'route_type',
        'distance_m',
        'is_accessible',
    )

    list_filter = (
        'route_type',
        'is_accessible',
    )

    search_fields = (
        'name',
        'description',
    )