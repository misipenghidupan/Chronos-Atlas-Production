import graphene
# Import schemas from the individual apps
from timeline.schema import TimelineQuery, TimelineMutation
from figures.schema import FigureQuery, FigureMutation

# Combine all application queries into a single root Query
class Query(TimelineQuery, FigureQuery, graphene.ObjectType):
    """The root query for the ChronosAtlas GraphQL API."""
    # Note: Fields are inherited from TimelineQuery and FigureQuery
    pass

# Combine all application mutations into a single root Mutation
class Mutation(TimelineMutation, FigureMutation, graphene.ObjectType):
    """The root mutation for the ChronosAtlas GraphQL API."""
    # Note: Fields are inherited from TimelineMutation (createTimelineEvent) 
    # and FigureMutation (createFigure)
    pass

# Create the final schema object, referenced in settings.py
schema = graphene.Schema(query=Query, mutation=Mutation)