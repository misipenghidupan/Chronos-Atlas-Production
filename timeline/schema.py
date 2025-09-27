import graphene
from graphene_django.types import DjangoObjectType
from .models import TimelineEvent
from django.db import IntegrityError

# --- 1. Graphene Type Definition ---
class TimelineEventType(DjangoObjectType):
    """Defines the structure of the TimelineEvent in GraphQL."""
    class Meta:
        model = TimelineEvent
        fields = ("id", "title", "year", "category", "description")

# --- 2. Query Definition ---
class TimelineQuery(graphene.ObjectType):
    """Handles fetching TimelineEvent data."""
    timelineEvents = graphene.List(TimelineEventType)
    
    def resolve_timelineEvents(root, info):
        """Resolver to fetch all TimelineEvent objects."""
        return TimelineEvent.objects.all()

# --- 3. Mutation Input Definition ---
class TimelineEventInput(graphene.InputObjectType):
    """Input structure for creating/updating a TimelineEvent."""
    title = graphene.String(required=True)
    year = graphene.Int(required=True)
    category = graphene.String(required=True)
    description = graphene.String(required=False)

# --- 4. Mutation Definition (Create Operation) ---
class CreateTimelineEvent(graphene.Mutation):
    """Mutation to create a new TimelineEvent."""
    # The output field after the mutation is performed
    timelineEvent = graphene.Field(TimelineEventType)

    class Arguments:
        # The input fields for the mutation
        input = TimelineEventInput(required=True)

    @staticmethod
    def mutate(root, info, input=None):
        try:
            timeline_event = TimelineEvent.objects.create(
                title=input.title,
                year=input.year,
                category=input.category,
                description=input.description if input.description else ""
            )
            return CreateTimelineEvent(timelineEvent=timeline_event)
        except IntegrityError as e:
            raise Exception(f"Database error while creating TimelineEvent: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")

# --- 5. Mutation Container ---
class TimelineMutation(graphene.ObjectType):
    """Root container for all Timeline-related mutations."""
    createTimelineEvent = CreateTimelineEvent.Field()
