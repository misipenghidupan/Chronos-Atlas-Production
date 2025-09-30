import graphene
from graphene_django import DjangoObjectType
from .models import TimelineEvent

# 1. Define the Graphene Type for the TimelineEvent model
class TimelineEventType(DjangoObjectType):
    class Meta:
        model = TimelineEvent
        fields = ("id", "title", "year", "category", "description")

# 2. Define a Query class for the timeline app
class Query(graphene.ObjectType):
    # Define a field to get a list of all timeline events
    all_timeline_events = graphene.List(TimelineEventType)

    # Define the resolver for the all_timeline_events field
    def resolve_all_timeline_events(root, info):
        # Return all TimelineEvent objects, letting the model's Meta.ordering handle sorting
        return TimelineEvent.objects.all()