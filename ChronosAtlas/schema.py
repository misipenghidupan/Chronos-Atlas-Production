import graphene
from timeline.schema import TimelineQuery, TimelineMutation
from figures.schema import FigureQuery, FigureMutation

class Query(TimelineQuery, FigureQuery, graphene.ObjectType):
    """
    The root GraphQL Query class. 
    It inherits all fields and resolvers from FigureQuery and TimelineQuery.
    """
    pass

class Mutation(TimelineMutation, FigureMutation, graphene.ObjectType):
    """
    The root GraphQL Mutation class.
    It combines mutations from all application schemas.
    """
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
