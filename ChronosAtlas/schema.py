import graphene

import figures.schema
import timeline.schema


# 1. Combine the app-specific queries into a single root Query.
# The order of inheritance matters if there are conflicting field names.
class Query(figures.schema.Query, timeline.schema.Query, graphene.ObjectType):
    # This class will inherit the fields from the other query classes.
    pass


# 2. Create the final schema object that Graphene-Django will use.
class Mutation(figures.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
