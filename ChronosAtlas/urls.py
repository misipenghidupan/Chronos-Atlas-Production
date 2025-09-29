from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from .views import home
from rest_framework import routers
from figures.api import FigureViewSet
from timeline.api import TimelineEventViewSet, InfluenceViewSet

router = routers.DefaultRouter()
router.register(r'figures', FigureViewSet)
router.register(r'timeline', TimelineEventViewSet)
router.register(r'influences', InfluenceViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]