import graphene
from graphene_django import DjangoObjectType
from .models import Figure

# 1. Define the Graphene Type for the Figure model
class FigureType(DjangoObjectType):
    class Meta:
        model = Figure
        # Explicitly define the fields to expose in the API
        fields = ("id", "name", "birthYear", "deathYear", "description")

# 2. Define a Query class for the figures app
class Query(graphene.ObjectType):
    # Define a field to get a list of all figures
    all_figures = graphene.List(FigureType)

    # Define the resolver for the all_figures field
    def resolve_all_figures(root, info):
        # Return all Figure objects, letting the model's Meta.ordering handle sorting
        return Figure.objects.all()