from django.core.management.base import BaseCommand
from django.contrib.gis.geos import (
    LineString,
    Point,
    Polygon,
)
from django.db import transaction

from places.models import Place
from routes.models import Route
from zones.models import Zone


class Command(BaseCommand):
    """
    Populate a small coherent demonstration dataset.

    The coordinates are intentionally grouped in one campus-sized
    area so spatial queries can be demonstrated clearly.
    """

    help = "Populate the database with sample campus spatial data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing campus data before loading",
        )

    @transaction.atomic
    def handle(self, *args, **options):

        if options["clear"]:
            self.stdout.write(
                "Removing existing campus data..."
            )

            Route.objects.all().delete()
            Zone.objects.all().delete()
            Place.objects.all().delete()

        self.stdout.write(
            "Creating campus places..."
        )

        places = [
            {
                "name": "Central Library",
                "description": (
                    "Main study and library facility."
                ),
                "category": "library",
                "lng": -6.2795,
                "lat": 53.3552,
                "opening_hours": "08:00-21:00",
                "is_accessible": True,
            },
            {
                "name": "Student Hub",
                "description": (
                    "Student support and social area."
                ),
                "category": "study",
                "lng": -6.2787,
                "lat": 53.3555,
                "opening_hours": "08:00-20:00",
                "is_accessible": True,
            },
            {
                "name": "Campus Cafe",
                "description": (
                    "Cafe serving drinks and food."
                ),
                "category": "cafe",
                "lng": -6.2800,
                "lat": 53.3548,
                "opening_hours": "08:00-17:00",
                "is_accessible": True,
            },
            {
                "name": "North Study Area",
                "description": (
                    "Quiet study location."
                ),
                "category": "study",
                "lng": -6.2791,
                "lat": 53.3561,
                "opening_hours": "09:00-20:00",
                "is_accessible": True,
            },
            {
                "name": "Print Station A",
                "description": (
                    "Student printing facility."
                ),
                "category": "printer",
                "lng": -6.2783,
                "lat": 53.3549,
                "opening_hours": "08:00-21:00",
                "is_accessible": True,
            },
            {
                "name": "Bike Parking North",
                "description": (
                    "Covered bicycle parking."
                ),
                "category": "bike",
                "lng": -6.2805,
                "lat": 53.3560,
                "opening_hours": "24 hours",
                "is_accessible": True,
            },
            {
                "name": "Accessibility Support",
                "description": (
                    "Accessibility support services."
                ),
                "category": "accessibility",
                "lng": -6.2779,
                "lat": 53.3556,
                "opening_hours": "09:00-17:00",
                "is_accessible": True,
            },
            {
                "name": "South Study Room",
                "description": (
                    "Group and individual study space."
                ),
                "category": "study",
                "lng": -6.2790,
                "lat": 53.3542,
                "opening_hours": "09:00-20:00",
                "is_accessible": True,
            },
            {
                "name": "South Cafe",
                "description": (
                    "Small student cafe."
                ),
                "category": "cafe",
                "lng": -6.2778,
                "lat": 53.3544,
                "opening_hours": "08:30-16:30",
                "is_accessible": False,
            },
            {
                "name": "Print Station B",
                "description": (
                    "Secondary student printing area."
                ),
                "category": "printer",
                "lng": -6.2802,
                "lat": 53.3540,
                "opening_hours": "09:00-18:00",
                "is_accessible": True,
            },
            {
                "name": "Bike Parking South",
                "description": (
                    "Outdoor bicycle parking."
                ),
                "category": "bike",
                "lng": -6.2810,
                "lat": 53.3538,
                "opening_hours": "24 hours",
                "is_accessible": True,
            },
            {
                "name": "Student Services",
                "description": (
                    "General student services office."
                ),
                "category": "other",
                "lng": -6.2774,
                "lat": 53.3550,
                "opening_hours": "09:00-17:00",
                "is_accessible": True,
            },
        ]

        for item in places:
            Place.objects.update_or_create(
                name=item["name"],
                defaults={
                    "description": item["description"],
                    "category": item["category"],
                    "location": Point(
                        item["lng"],
                        item["lat"],
                        srid=4326,
                    ),
                    "opening_hours": (
                        item["opening_hours"]
                    ),
                    "is_accessible": (
                        item["is_accessible"]
                    ),
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Places loaded: {Place.objects.count()}"
            )
        )

        self.stdout.write(
            "Creating campus zones..."
        )

        campus_boundary = Polygon(
            (
                (-6.2815, 53.3534),
                (-6.2768, 53.3534),
                (-6.2768, 53.3565),
                (-6.2815, 53.3565),
                (-6.2815, 53.3534),
            ),
            srid=4326,
        )

        north_zone = Polygon(
            (
                (-6.2810, 53.3552),
                (-6.2772, 53.3552),
                (-6.2772, 53.3564),
                (-6.2810, 53.3564),
                (-6.2810, 53.3552),
            ),
            srid=4326,
        )

        south_zone = Polygon(
            (
                (-6.2812, 53.3536),
                (-6.2770, 53.3536),
                (-6.2770, 53.3551),
                (-6.2812, 53.3551),
                (-6.2812, 53.3536),
            ),
            srid=4326,
        )

        green_zone = Polygon(
            (
                (-6.2808, 53.3547),
                (-6.2796, 53.3547),
                (-6.2796, 53.3554),
                (-6.2808, 53.3554),
                (-6.2808, 53.3547),
            ),
            srid=4326,
        )

        Zone.objects.update_or_create(
            name="Main Campus",
            defaults={
                "description": (
                    "Main demonstration campus boundary."
                ),
                "zone_type": "campus",
                "boundary": campus_boundary,
            },
        )

        Zone.objects.update_or_create(
            name="North Accessible Zone",
            defaults={
                "description": (
                    "Northern accessible campus area."
                ),
                "zone_type": "accessible",
                "boundary": north_zone,
            },
        )

        Zone.objects.update_or_create(
            name="South Pedestrian Zone",
            defaults={
                "description": (
                    "Pedestrian-focused southern campus area."
                ),
                "zone_type": "pedestrian",
                "boundary": south_zone,
            },
        )

        Zone.objects.update_or_create(
            name="Central Green Space",
            defaults={
                "description": (
                    "Central green and recreation space."
                ),
                "zone_type": "green",
                "boundary": green_zone,
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Zones loaded: {Zone.objects.count()}"
            )
        )

        self.stdout.write(
            "Creating campus routes..."
        )

        routes = [
            {
                "name": "North-South Walking Route",
                "description": (
                    "Main pedestrian connection "
                    "through the campus."
                ),
                "route_type": "walking",
                "distance_m": 330,
                "is_accessible": True,
                "coordinates": [
                    (-6.2796, 53.3562),
                    (-6.2793, 53.3554),
                    (-6.2790, 53.3546),
                    (-6.2788, 53.3538),
                ],
            },
            {
                "name": "Accessible East Route",
                "description": (
                    "Accessible route connecting "
                    "eastern facilities."
                ),
                "route_type": "accessible",
                "distance_m": 280,
                "is_accessible": True,
                "coordinates": [
                    (-6.2780, 53.3560),
                    (-6.2781, 53.3554),
                    (-6.2780, 53.3548),
                    (-6.2778, 53.3541),
                ],
            },
            {
                "name": "West Walking Route",
                "description": (
                    "Walking route along the "
                    "western side of campus."
                ),
                "route_type": "walking",
                "distance_m": 310,
                "is_accessible": False,
                "coordinates": [
                    (-6.2807, 53.3561),
                    (-6.2804, 53.3553),
                    (-6.2804, 53.3546),
                    (-6.2807, 53.3538),
                ],
            },
            {
                "name": "Central Cycle Route",
                "description": (
                    "Cycle route crossing the "
                    "central campus area."
                ),
                "route_type": "cycling",
                "distance_m": 420,
                "is_accessible": True,
                "coordinates": [
                    (-6.2810, 53.3550),
                    (-6.2798, 53.3550),
                    (-6.2786, 53.3550),
                    (-6.2772, 53.3550),
                ],
            },
        ]

        for item in routes:
            Route.objects.update_or_create(
                name=item["name"],
                defaults={
                    "description": item["description"],
                    "route_type": item["route_type"],
                    "path": LineString(
                        item["coordinates"],
                        srid=4326,
                    ),
                    "distance_m": item["distance_m"],
                    "is_accessible": (
                        item["is_accessible"]
                    ),
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Routes loaded: {Route.objects.count()}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "\nCampus data population completed successfully."
            )
        )

        self.stdout.write(
            f"Places: {Place.objects.count()}"
        )

        self.stdout.write(
            f"Routes: {Route.objects.count()}"
        )

        self.stdout.write(
            f"Zones: {Zone.objects.count()}"
        )