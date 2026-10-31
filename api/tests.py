from django.contrib.gis.geos import (
    LineString,
    Point,
    Polygon,
)

from rest_framework import status
from rest_framework.test import APITestCase

from places.models import Place
from routes.models import Route
from zones.models import Zone


class SpatialAPITests(APITestCase):

    def setUp(self):

        self.place = Place.objects.create(
            name="Test Library",
            description="Test facility",
            category="library",
            location=Point(
                -6.2795,
                53.3552,
                srid=4326,
            ),
            opening_hours="09:00-17:00",
            is_accessible=True,
        )

        self.nearby_place = Place.objects.create(
            name="Nearby Cafe",
            description="Nearby test facility",
            category="cafe",
            location=Point(
                -6.2790,
                53.3553,
                srid=4326,
            ),
            opening_hours="09:00-17:00",
            is_accessible=True,
        )

        self.zone = Zone.objects.create(
            name="Test Campus",
            description="Test zone",
            zone_type="campus",
            boundary=Polygon(
                (
                    (-6.2810, 53.3540),
                    (-6.2770, 53.3540),
                    (-6.2770, 53.3560),
                    (-6.2810, 53.3560),
                    (-6.2810, 53.3540),
                ),
                srid=4326,
            ),
        )

        self.route = Route.objects.create(
            name="Test Walking Route",
            description="Test route",
            route_type="walking",
            path=LineString(
                (
                    -6.2805,
                    53.3550,
                ),
                (
                    -6.2775,
                    53.3550,
                ),
                srid=4326,
            ),
            distance_m=200,
            is_accessible=True,
        )

    def test_places_list(self):

        response = self.client.get(
            "/api/places/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_routes_list(self):

        response = self.client.get(
            "/api/routes/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_zones_list(self):

        response = self.client.get(
            "/api/zones/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_nearest_places(self):

        response = self.client.get(
            "/api/places/nearest/",
            {
                "lat": 53.3552,
                "lng": -6.2795,
                "limit": 2,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data["features"]),
            2,
        )

    def test_within_radius(self):

        response = self.client.get(
            "/api/places/within-radius/",
            {
                "lat": 53.3552,
                "lng": -6.2795,
                "radius": 500,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertGreaterEqual(
            len(response.data["features"]),
            1,
        )

    def test_point_in_polygon(self):

        response = self.client.get(
            "/api/zones/contains-point/",
            {
                "lat": 53.3550,
                "lng": -6.2790,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertGreaterEqual(
            len(response.data["features"]),
            1,
        )

    def test_route_intersection(self):

        response = self.client.get(
            "/api/routes/intersecting-zone/",
            {
                "zone_id": self.zone.id,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertGreaterEqual(
            len(response.data["features"]),
            1,
        )

    def test_invalid_latitude(self):

        response = self.client.get(
            "/api/places/nearest/",
            {
                "lat": 100,
                "lng": -6.27,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_missing_coordinates(self):

        response = self.client.get(
            "/api/places/nearest/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_negative_radius(self):

        response = self.client.get(
            "/api/places/within-radius/",
            {
                "lat": 53.35,
                "lng": -6.27,
                "radius": -100,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_missing_zone(self):

        response = self.client.get(
            "/api/routes/intersecting-zone/",
            {
                "zone_id": 99999,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )