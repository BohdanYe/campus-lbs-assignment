from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    PlaceViewSet,
    RouteViewSet,
    ZoneViewSet,
)


router = DefaultRouter()

router.register(
    r"places",
    PlaceViewSet,
    basename="place",
)

router.register(
    r"routes",
    RouteViewSet,
    basename="route",
)

router.register(
    r"zones",
    ZoneViewSet,
    basename="zone",
)


urlpatterns = [
    path("", include(router.urls)),
]