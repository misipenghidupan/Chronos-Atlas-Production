from rest_framework import routers
from django.urls import include, path

# These imports are NOW SAFE
from .api import InfluenceViewSet, TimelineEventViewSet

router = routers.DefaultRouter()
router.register(r"timeline", TimelineEventViewSet)
router.register(r"influences", InfluenceViewSet)

urlpatterns = [
    path("", include(router.urls)),
]