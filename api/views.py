from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from places.models import Place
from routes.models import Route
from zones.models import Zone

from .serializers import (
    PlaceSerializer,
    RouteSerializer,
    ZoneSerializer,
)


def parse_coordinates(request):
    """
    Read and validate latitude and longitude from query parameters.

    Returns:
        (Point, None) when valid
        (None, Response) when invalid
    """

    lat = request.query_params.get("lat")
    lng = request.query_params.get("lng")

    if lat is None or lng is None:
        return None, Response(
            {
                "error": (
                    "Both lat and lng query parameters are required."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        lat = float(lat)
        lng = float(lng)

    except (TypeError, ValueError):
        return None, Response(
            {
                "error": (
                    "Latitude and longitude must be numeric values."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not -90 <= lat <= 90:
        return None, Response(
            {
                "error": (
                    "Latitude must be between -90 and 90."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not -180 <= lng <= 180:
        return None, Response(
            {
                "error": (
                    "Longitude must be between -180 and 180."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    point = Point(
        lng,
        lat,
        srid=4326,
    )

    return point, None


class PlaceViewSet(viewsets.ModelViewSet):
    """
    CRUD API for campus places.

    Spatial endpoints:
    - nearest
    - within-radius
    """

    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    filterset_fields = [
        "category",
        "is_accessible",
    ]

    search_fields = [
        "name",
        "description",
    ]

    ordering_fields = [
        "name",
        "category",
        "created_at",
    ]

    @action(
        detail=False,
        methods=["get"],
        url_path="nearest",
    )
    def nearest(self, request):
        """
        Find the nearest places to a latitude/longitude.

        Example:
        /api/places/nearest/?lat=53.355&lng=-6.279&limit=5
        """

        point, error_response = parse_coordinates(request)

        if error_response:
            return error_response

        limit = request.query_params.get("limit", 5)

        try:
            limit = int(limit)

        except (TypeError, ValueError):
            return Response(
                {
                    "error": "limit must be an integer."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if limit < 1 or limit > 50:
            return Response(
                {
                    "error": (
                        "limit must be between 1 and 50."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        places = (
            Place.objects
            .annotate(
                distance=Distance(
                    "location",
                    point,
                )
            )
            .order_by("distance")[:limit]
        )

        serializer = self.get_serializer(
            places,
            many=True,
        )

        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="within-radius",
    )
    def within_radius(self, request):
        """
        Find places within a radius in metres.

        Example:
        /api/places/within-radius/
        ?lat=53.355&lng=-6.279&radius=500
        """

        point, error_response = parse_coordinates(request)

        if error_response:
            return error_response

        radius = request.query_params.get(
            "radius",
            500,
        )

        try:
            radius = float(radius)

        except (TypeError, ValueError):
            return Response(
                {
                    "error": (
                        "radius must be a numeric value."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if radius <= 0:
            return Response(
                {
                    "error": (
                        "radius must be greater than 0 metres."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if radius > 10000:
            return Response(
                {
                    "error": (
                        "radius cannot be greater than "
                        "10000 metres."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        places = (
            Place.objects
            .filter(
                location__distance_lte=(
                    point,
                    D(m=radius),
                )
            )
            .annotate(
                distance=Distance(
                    "location",
                    point,
                )
            )
            .order_by("distance")
        )

        serializer = self.get_serializer(
            places,
            many=True,
        )

        return Response(serializer.data)


class ZoneViewSet(viewsets.ModelViewSet):
    """
    CRUD API for campus zones.

    Spatial endpoint:
    - contains-point
    """

    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

    filterset_fields = [
        "zone_type",
    ]

    search_fields = [
        "name",
        "description",
    ]

    ordering_fields = [
        "name",
        "zone_type",
    ]

    @action(
        detail=False,
        methods=["get"],
        url_path="contains-point",
    )
    def contains_point(self, request):
        """
        Find zones containing a supplied point.

        Example:
        /api/zones/contains-point/
        ?lat=53.355&lng=-6.279
        """

        point, error_response = parse_coordinates(request)

        if error_response:
            return error_response

        zones = Zone.objects.filter(
            boundary__contains=point
        )

        serializer = self.get_serializer(
            zones,
            many=True,
        )

        return Response(serializer.data)


class RouteViewSet(viewsets.ModelViewSet):
    """
    CRUD API for campus routes.

    Spatial endpoint:
    - intersecting-zone
    """

    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    filterset_fields = [
        "route_type",
        "is_accessible",
    ]

    search_fields = [
        "name",
        "description",
    ]

    ordering_fields = [
        "name",
        "route_type",
        "distance_m",
    ]

    @action(
        detail=False,
        methods=["get"],
        url_path="intersecting-zone",
    )
    def intersecting_zone(self, request):
        """
        Find all routes that intersect a selected zone.

        Example:
        /api/routes/intersecting-zone/?zone_id=1
        """

        zone_id = request.query_params.get(
            "zone_id"
        )

        if not zone_id:
            return Response(
                {
                    "error": (
                        "zone_id query parameter is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            zone_id = int(zone_id)

        except (TypeError, ValueError):
            return Response(
                {
                    "error": (
                        "zone_id must be an integer."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            zone = Zone.objects.get(
                pk=zone_id
            )

        except Zone.DoesNotExist:
            return Response(
                {
                    "error": (
                        "The requested zone does not exist."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        routes = Route.objects.filter(
            path__intersects=zone.boundary
        )

        serializer = self.get_serializer(
            routes,
            many=True,
        )

        return Response(serializer.data)