from django.contrib.gis.db import models


class Zone(models.Model):

    ZONE_TYPE_CHOICES = [
        ('campus', 'Campus'),
        ('pedestrian', 'Pedestrian Area'),
        ('study', 'Study Zone'),
        ('restricted', 'Restricted Area'),
        ('accessible', 'Accessible Area'),
        ('green', 'Green Space'),
    ]

    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    zone_type = models.CharField(
        max_length=30,
        choices=ZONE_TYPE_CHOICES,
        default='campus'
    )

    # Spatial Polygon
    boundary = models.PolygonField(
        srid=4326,
        spatial_index=True
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
                fields=['zone_type']
            ),
        ]