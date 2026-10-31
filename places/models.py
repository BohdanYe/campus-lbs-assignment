from django.contrib.gis.db import models


class Place(models.Model):

    CATEGORY_CHOICES = [
        ('library', 'Library'),
        ('cafe', 'Cafe'),
        ('study', 'Study Area'),
        ('printer', 'Printer'),
        ('bike', 'Bike Parking'),
        ('accessibility', 'Accessibility Service'),
        ('other', 'Other'),
    ]

    name = models.CharField(
        max_length=150
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