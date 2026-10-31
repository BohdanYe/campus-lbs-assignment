from django.contrib.gis.db import models


class Route(models.Model):

    ROUTE_TYPE_CHOICES = [
        ('walking', 'Walking'),
        ('accessible', 'Accessible'),
        ('cycling', 'Cycling'),
    ]

    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    route_type = models.CharField(
        max_length=30,
        choices=ROUTE_TYPE_CHOICES,
        default='walking'
    )

    # Spatial Line
    path = models.LineStringField(
        srid=4326,
        spatial_index=True
    )

    distance_m = models.FloatField(
        null=True,
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
                fields=['route_type']
            ),
        ]