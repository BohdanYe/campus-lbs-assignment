from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from places.models import Place
from routes.models import Route
from zones.models import Zone


class PlaceSerializer(GeoFeatureModelSerializer):
    """
    Serialize Place objects as GeoJSON point features.

    distance_m is included when the queryset has been annotated
    with a distance value, for example in nearest/radius searches.
    """

    distance_m = serializers.SerializerMethodField()

    class Meta:
        model = Place
        geo_field = "location"

        fields = [
            "id",
            "name",
            "description",
            "category",
            "opening_hours",
            "is_accessible",
            "distance_m",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "distance_m",
        ]

    def get_distance_m(self, obj):
        distance = getattr(obj, "distance", None)

        if distance is None:
            return None

        return round(distance.m, 2)


class RouteSerializer(GeoFeatureModelSerializer):
    """
    Serialize Route objects as GeoJSON LineString features.
    """

    class Meta:
        model = Route
        geo_field = "path"

        fields = [
            "id",
            "name",
            "description",
            "route_type",
            "distance_m",
            "is_accessible",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class ZoneSerializer(GeoFeatureModelSerializer):
    """
    Serialize Zone objects as GeoJSON Polygon features.
    """

    class Meta:
        model = Zone
        geo_field = "boundary"

        fields = [
            "id",
            "name",
            "description",
            "zone_type",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]