from rest_framework import routers
from django.urls import include, path

# These imports are NOW SAFE because they only happen when 'figures.urls' is included
from .api import FigureViewSet 

router = routers.DefaultRouter()
router.register(r"figures", FigureViewSet)

urlpatterns = [
    path("", include(router.urls)),
]