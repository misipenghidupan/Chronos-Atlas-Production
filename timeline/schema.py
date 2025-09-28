import graphene
from graphene_django.types import DjangoObjectType
from .models import TimelineEvent

# --- 1. Graphene Type Definition (Read Schema) ---

class TimelineEventType(DjangoObjectType):
    """
    Defines the GraphQL object representation for the TimelineEvent model.
    """
    class Meta:
        model = TimelineEvent
        fields = ('id', 'title', 'year', 'category', 'description')
        # Setting interfaces is good practice, especially if using Relay, 
        # but not strictly required for basic Graphene setup.
        # interfaces = (graphene.Node,)

# --- 2. Query Definition (Read Operations) ---

class TimelineQuery(graphene.ObjectType):
    """
    Defines the query fields for fetching TimelineEvent data.
    """
    # Query to fetch a list of all events
    all_timeline_events = graphene.List(TimelineEventType)

    # Query to fetch a single event by its ID
    timeline_event = graphene.Field(
        TimelineEventType,
        id=graphene.Int() # Using Int for the primary key lookup
    )

    def resolve_all_timeline_events(root, info):
        """Returns all TimelineEvent objects, ordered by year (as defined in models.py)."""
        return TimelineEvent.objects.all()

    def resolve_timeline_event(root, info, id):
        """Returns a single TimelineEvent object based on the provided ID."""
        try:
            return TimelineEvent.objects.get(pk=id)
        except TimelineEvent.DoesNotExist:
            return None

# --- 3. Mutation Definition (Write Operations) ---

class TimelineEventInput(graphene.InputObjectType):
    """
    Input structure for creating or updating a TimelineEvent. 
    Matches the required fields on the model.
    """
    title = graphene.String(required=True)
    year = graphene.Int(required=True)
    category = graphene.String(required=True)
    description = graphene.String(required=False)

class CreateTimelineEvent(graphene.Mutation):
    """
    Mutation for creating a new TimelineEvent.
    Uses the standard Graphene input pattern confirmed in the last successful mutation.
    """
    class Arguments:
        # Accepts the single 'input' object defined above
        input = TimelineEventInput(required=True)

    # Defines the fields returned after a successful mutation
    timeline_event = graphene.Field(TimelineEventType)

    @staticmethod
    def mutate(root, info, input=None):
        """Performs the creation operation."""
        # Create the model instance using the input data
        timeline_event = TimelineEvent.objects.create(
            title=input.title,
            year=input.year,
            category=input.category,
            description=input.description if hasattr(input, 'description') else None
        )
        
        # Return the mutation payload
        return CreateTimelineEvent(timeline_event=timeline_event)

class TimelineMutation(graphene.ObjectType):
    """
    Combines all write operations for the timeline app.
    """
    create_timeline_event = CreateTimelineEvent.Field()
    # Add update_timeline_event and delete_timeline_event fields later