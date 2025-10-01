import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .filters import TimelineEventFilter
from .models import Influence, TimelineEvent


# 1. Define the Graphene Type for the Influence model
class InfluenceType(DjangoObjectType):
    class Meta:
        model = Influence
        fields = ("id", "influencer", "influenced")
        interfaces = (graphene.relay.Node,)
        filter_fields = []


# 1. Define the Graphene Type for the TimelineEvent model
class TimelineEventType(DjangoObjectType):
    class Meta:
        model = TimelineEvent
        fields = ("id", "title", "year", "category", "description")
        interfaces = (graphene.relay.Node,)


# 2. Define a Query class for the timeline app
class Query(graphene.ObjectType):
    # Use DjangoFilterConnectionField to enable pagination and filtering
    all_timeline_events = DjangoFilterConnectionField(
        TimelineEventType, filterset_class=TimelineEventFilter
    )
    # Apply pagination to the influences query as well
    all_influences = DjangoFilterConnectionField(InfluenceType)
