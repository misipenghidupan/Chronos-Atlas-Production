from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from .views import home

# 1. REMOVE ALL ViewSet IMPORTS HERE:
# from figures.api import FigureViewSet
# from timeline.api import InfluenceViewSet, TimelineEventViewSet

# 2. REMOVE THE ROUTER DEFINITIONS HERE:
# router = routers.DefaultRouter()
# router.register(r"figures", FigureViewSet)
# router.register(r"timeline", TimelineEventViewSet)
# router.register(r"influences", InfluenceViewSet)


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    # 3. INCLUDE THE NEW APP-LEVEL URLS FILES:
    path("api/", include("figures.urls")),  # New figure API endpoints
    path("api/", include("timeline.urls")),  # New timeline API endpoints
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
