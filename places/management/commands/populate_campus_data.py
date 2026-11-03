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
                "name": "Academic Hub & Library",
                "building_code": "AH",
                "description": (
                    "TU Dublin's main Grangegorman library and academic support hub. "
                    "Includes study spaces, learning supports, event space and a cafe."
                ),
                "category": "library",
                "lng": -6.2809,
                "lat": 53.3562,
                "opening_hours": "Term time: Library generally 09:00-21:00 Mon-Thu",
                "is_accessible": True,
            },
            {
                "name": "Central Quad",
                "building_code": "CQ",
                "description": (
                    "Major teaching building containing science, computing, engineering, "
                    "culinary arts and other academic facilities."
                ),
                "category": "academic",
                "lng": -6.2789,
                "lat": 53.3560,
                "opening_hours": "Term time: 08:00-22:00 Mon-Thu",
                "is_accessible": True,
            },
            {
                "name": "East Quad",
                "building_code": "EQ",
                "description": (
                    "Academic building for media, social sciences, creative arts, "
                    "music and drama."
                ),
                "category": "academic",
                "lng": -6.2764,
                "lat": 53.3538,
                "opening_hours": "Term time: 08:00-22:00 Mon-Thu",
                "is_accessible": True,
            },
            {
                "name": "Lower House",
                "building_code": "LH",
                "description": (
                    "Campus building containing student facilities, common rooms, "
                    "fitness spaces and student union services."
                ),
                "category": "student_services",
                "lng": -6.2782,
                "lat": 53.3527,
                "opening_hours": "Term time: 08:00-22:00 Mon-Thu",
                "is_accessible": True,
            },
            {
                "name": "Rathdown House",
                "building_code": "RD",
                "description": (
                    "Student services building containing the Student Hub, "
                    "Student Health Centre and counselling services."
                ),
                "category": "student_services",
                "lng": -6.2800,
                "lat": 53.3551,
                "opening_hours": "Term time: 08:00-22:00 Mon-Thu",
                "is_accessible": True,
            },
            {
                "name": "Student Health Centre",
                "description": (
                    "TU Dublin student health and counselling services located "
                    "in Rathdown House."
                ),
                "category": "health",
                "lng": -6.2800,
                "lat": 53.3550,
                "opening_hours": "Check current TU Dublin service hours",
                "is_accessible": True,
            },
            {
                "name": "Glassmanogue Gym",
                "description": (
                    "University gym with fitness equipment, changing facilities "
                    "and access to sports programmes."
                ),
                "category": "sports",
                "lng": -6.2818,
                "lat": 53.3552,
                "opening_hours": "Term time building hours vary",
                "is_accessible": True,
            },
            {
                "name": "Greenway Hub",
                "description": (
                    "Campus building located close to the central academic area."
                ),
                "category": "academic",
                "lng": -6.2793,
                "lat": 53.3554,
                "opening_hours": "Term time: 08:00-22:00 Mon-Thu",
                "is_accessible": True,
            },
            {
                "name": "National Optometry Centre",
                "description": (
                    "Purpose-built optometry teaching and public clinical facility."
                ),
                "category": "health",
                "lng": -6.2798,
                "lat": 53.3556,
                "opening_hours": "Check current clinic opening hours",
                "is_accessible": True,
            },
            {
                "name": "St. Laurence",
                "description": (
                    "Centre for prayer, worship, culture, spiritual development "
                    "and events."
                ),
                "category": "community",
                "lng": -6.2810,
                "lat": 53.3548,
                "opening_hours": "Check current campus schedule",
                "is_accessible": True,
            },
            {
                "name": "The Golden Bandstand",
                "description": (
                    "Outdoor campus landmark and event space."
                ),
                "category": "heritage",
                "lng": -6.2797,
                "lat": 53.3555,
                "opening_hours": "Campus grounds hours",
                "is_accessible": True,
            },
            {
                "name": "Park House",
                "description": (
                    "Campus building located on the northern side of Grangegorman."
                ),
                "category": "academic",
                "lng": -6.2830,
                "lat": 53.3575,
                "opening_hours": "Typically 08:00-18:00",
                "is_accessible": True,
            },
            {
                "name": "Bradogue",
                "description": (
                    "Campus building containing student support and union-related facilities."
                ),
                "category": "student_services",
                "lng": -6.2790,
                "lat": 53.3545,
                "opening_hours": "Term time: 08:00-22:00 Mon-Thu",
                "is_accessible": True,
            },
            {
                "name": "Printmaking Workshop",
                "description": (
                    "Specialist printmaking workshop on the Grangegorman campus."
                ),
                "category": "academic",
                "lng": -6.2769,
                "lat": 53.3546,
                "opening_hours": "Academic access hours",
                "is_accessible": True,
            },
            {
                "name": "Clocktower",
                "description": (
                    "Historic landmark building within the Grangegorman campus."
                ),
                "category": "heritage",
                "lng": -6.2803,
                "lat": 53.3544,
                "opening_hours": "Campus access hours",
                "is_accessible": True,
            },
            {
                "name": "Training Restaurants",
                "description": (
                    "Training restaurant facilities associated with Central Quad "
                    "and hospitality education."
                ),
                "category": "cafe",
                "lng": -6.2787,
                "lat": 53.3558,
                "opening_hours": "Reservations / academic schedule",
                "is_accessible": True,
            },
        ]

        for item in places:
            Place.objects.update_or_create(
                name=item["name"],
                defaults={
                    "building_code": item.get("building_code", ""),
                    "description": item["description"],
                    "category": item["category"],
                    "location": Point(
                        item["lng"],
                        item["lat"],
                        srid=4326,
                    ),
                    "opening_hours": item["opening_hours"],
                    "is_accessible": item["is_accessible"],
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
                (-6.2842, 53.3583),
                (-6.2816, 53.3587),
                (-6.2793, 53.3584),
                (-6.2763, 53.3572),
                (-6.2748, 53.3547),
                (-6.2753, 53.3523),
                (-6.2779, 53.3516),
                (-6.2812, 53.3521),
                (-6.2835, 53.3536),
                (-6.2845, 53.3560),
                (-6.2842, 53.3583),
            ),
            srid=4326,
        )

        academic_core = Polygon(
            (
                (-6.2812, 53.3546),
                (-6.2772, 53.3546),
                (-6.2769, 53.3565),
                (-6.2808, 53.3568),
                (-6.2812, 53.3546),
            ),
            srid=4326,
        )

        sports_area = Polygon(
            (
                (-6.2831, 53.3534),
                (-6.2795, 53.3534),
                (-6.2794, 53.3553),
                (-6.2825, 53.3556),
                (-6.2831, 53.3534),
            ),
            srid=4326,
        )

        south_campus = Polygon(
            (
                (-6.2794, 53.3518),
                (-6.2756, 53.3519),
                (-6.2753, 53.3545),
                (-6.2793, 53.3546),
                (-6.2794, 53.3518),
            ),
            srid=4326,
        )

        Zone.objects.update_or_create(
            name="Main Campus",
            defaults={
                "description": (
                    "Approximate outer boundary of the TU Dublin "
                    "Grangegorman campus."
                ),
                "zone_type": "campus",
                "boundary": campus_boundary,
            },
        )

        Zone.objects.update_or_create(
            name="Academic Core",
            defaults={
                "description": (
                    "Central academic area around Central Quad, "
                    "Academic Hub and nearby facilities."
                ),
                "zone_type": "study",
                "boundary": academic_core,
            },
        )

        Zone.objects.update_or_create(
            name="Sports Area",
            defaults={
                "description": (
                    "Approximate area containing the main campus "
                    "sports pitches and related facilities."
                ),
                "zone_type": "green",
                "boundary": sports_area,
            },
        )

        Zone.objects.update_or_create(
            name="South Campus",
            defaults={
                "description": (
                    "Approximate southern section around East Quad "
                    "and Lower House."
                ),
                "zone_type": "pedestrian",
                "boundary": south_campus,
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
                "name": "North-South Campus Walk",
                "description": (
                    "Approximate pedestrian route connecting "
                    "the northern campus to East Quad."
                ),
                "route_type": "walking",
                "distance_m": 850,
                "is_accessible": True,
                "coordinates": [
                    (-6.2828, 53.3577),
                    (-6.2815, 53.3569),
                    (-6.2802, 53.3560),
                    (-6.2792, 53.3553),
                    (-6.2784, 53.3545),
                    (-6.2772, 53.3538),
                    (-6.2765, 53.3535),
                ],
            },
            {
                "name": "Central Accessible Route",
                "description": (
                    "Approximate accessible route through the "
                    "central academic area."
                ),
                "route_type": "accessible",
                "distance_m": 520,
                "is_accessible": True,
                "coordinates": [
                    (-6.2810, 53.3559),
                    (-6.2801, 53.3557),
                    (-6.2791, 53.3556),
                    (-6.2780, 53.3554),
                    (-6.2772, 53.3548),
                ],
            },
            {
                "name": "Sports Area Walk",
                "description": (
                    "Approximate pedestrian route along the "
                    "campus sports area."
                ),
                "route_type": "walking",
                "distance_m": 600,
                "is_accessible": True,
                "coordinates": [
                    (-6.2828, 53.3549),
                    (-6.2820, 53.3541),
                    (-6.2808, 53.3536),
                    (-6.2796, 53.3535),
                ],
            },
            {
                "name": "East Quad Cycle Connection",
                "description": (
                    "Approximate cycling connection toward East Quad."
                ),
                "route_type": "cycling",
                "distance_m": 470,
                "is_accessible": True,
                "coordinates": [
                    (-6.2800, 53.3551),
                    (-6.2787, 53.3548),
                    (-6.2775, 53.3542),
                    (-6.2764, 53.3537),
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