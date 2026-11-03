from django.contrib.gis.db import models


class Place(models.Model):

    CATEGORY_CHOICES = [
        ("academic", "Academic Building"),
        ("library", "Library"),
        ("student_services", "Student Services"),
        ("health", "Health Service"),
        ("sports", "Sports Facility"),
        ("cafe", "Cafe / Catering"),
        ("study", "Study Area"),
        ("accessibility", "Accessibility Service"),
        ("transport", "Transport"),
        ("heritage", "Heritage / Landmark"),
        ("community", "Community Facility"),
        ("other", "Other"),
    ]

    name = models.CharField(
        max_length=150
    )

    building_code = models.CharField(
        max_length=10,
        blank=True,
        default=""
    )
    
    description = models.TextField(
        blank=True
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='other'
    )

    # Spatial Point
    location = models.PointField(
        srid=4326,
        spatial_index=True
    )

    opening_hours = models.CharField(
        max_length=100,
        blank=True
    )

    is_accessible = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

        indexes = [
            models.Index(
                fields=['category']
            ),
        ]