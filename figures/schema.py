import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .filters import FigureFilter # Import the new filter
from .models import Figure, Field

# 1. Define the Graphene Type for the Field model
class FieldType(DjangoObjectType):
    class Meta:
        model = Field
        fields = ("id", "name")

# 1. Define the Graphene Type for the Figure model
class FigureType(DjangoObjectType):
    class Meta:
        model = Figure
        # Explicitly define the fields to expose in the API
        fields = ("id", "name", "slug", "summary", "birth_date", "death_date", "normalized_birth_year", "normalized_death_year", "fields")
        # Implement the Node interface for Relay-style pagination
        interfaces = (graphene.relay.Node,)

# 2. Define a Query class for the figures app
class Query(graphene.ObjectType):
    # Use DjangoFilterConnectionField to enable pagination and filtering
    all_figures = DjangoFilterConnectionField(FigureType, filterset_class=FigureFilter)
    
    # Add a new field to fetch a single figure by its slug
    figure_by_slug = graphene.Field(FigureType, slug=graphene.String(required=True))
    
    all_fields = graphene.List(FieldType)

    # Define the resolver for the all_fields field
    def resolve_all_fields(root, info):
        # Return all Field objects
        return Field.objects.all()

    # Define the resolver for the new figure_by_slug field
    def resolve_figure_by_slug(root, info, slug):
        """
        Resolver to fetch a single Figure instance by its unique slug.
        """
        try:
            return Figure.objects.get(slug=slug)
        except Figure.DoesNotExist:
            return None