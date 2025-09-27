import graphene
from graphene_django import DjangoObjectType
from .models import Figure # Note the relative import

class FigureType(DjangoObjectType):
    """GraphQL type definition for the Figure model."""
    class Meta:
        model = Figure
        fields = ('id', 'name', 'birthYear', 'deathYear', 'description')

class FigureQuery(graphene.ObjectType):
    """
    Defines the root query fields related to Figure data.
    """
    figures = graphene.List(FigureType)
    
    def resolve_figures(root, info):
        return Figure.objects.all()
    
    figure = graphene.Field(FigureType, id=graphene.Int(required=True))
    
    def resolve_figure(root, info, id):
        try:
            return Figure.objects.get(pk=id)
        except Figure.DoesNotExist:
            return None