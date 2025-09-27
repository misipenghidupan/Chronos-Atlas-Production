import graphene
from timeline.schema import Query as TimelineQuery

# Combine all application-specific queries into the root Query class
class Query(TimelineQuery, graphene.ObjectType):
    # This class will inherit all fields and resolvers from TimelineQuery
    pass

schema = graphene.Schema(query=Query)