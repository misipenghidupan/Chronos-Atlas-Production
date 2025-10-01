from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework import routers

from figures.api import FigureViewSet
from timeline.api import InfluenceViewSet, TimelineEventViewSet

from .views import home

router = routers.DefaultRouter()
router.register(r"figures", FigureViewSet)
router.register(r"timeline", TimelineEventViewSet)
router.register(r"influences", InfluenceViewSet)

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
