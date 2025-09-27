import graphene
from graphene_django.types import DjangoObjectType
from django.db.models import Q
from datetime import datetime
from .models import Figure, Field, Influence

# --- Types ---

class FieldType(DjangoObjectType):
    class Meta:
        model = Field
        fields = ("id", "name")

class FigureType(DjangoObjectType):
    # Expose M2M fields
    fields = graphene.List(FieldType)
    
    # Expose reverse FK for influences
    influenced_by = graphene.List(lambda: FigureType)

    class Meta:
        model = Figure
        fields = (
            "id",
            "name",
            "description",
            "birth_year",
            "death_year",
            # Custom resolvers will handle 'fields' and 'influenced_by'
        )

    def resolve_fields(self, info):
        return self.fields.all()

    def resolve_influenced_by(self, info):
        # Fetches the *influencers* who influenced *this* figure
        return [
            inf.influencer
            for inf in self.influenced_by_set.all().select_related("influencer")
        ]

# --- Queries ---

class Query(graphene.ObjectType):
    # Query 1: Master Timeline View
    figures = graphene.List(
        FigureType,
        min_year=graphene.Int(required=False),
        max_year=graphene.Int(required=False),
    )

    # Query 2: Figure Detail View
    figure = graphene.Field(
        FigureType, 
        id=graphene.Int(required=False), 
        name=graphene.String(required=False)
    )

    def resolve_figures(self, info, min_year=None, max_year=None):
        queryset = Figure.objects.all().prefetch_related('fields')
        
        # Default max_year to current year if not provided
        current_year = datetime.now().year
        
        if min_year is not None and max_year is not None:
            # Core Lifespan Overlap Filtering Logic:
            
            # 1. Non-living figures
            q_non_living = Q(
                birth_year__lte=max_year, 
                death_year__gte=min_year, 
                death_year__isnull=False
            )
            
            # 2. Living figures (death_year__isnull=True)
            # Treat their death year as the current year for the filter.
            q_living = Q(
                birth_year__lte=max_year,
                death_year__isnull=True
            )
            
            # Combine filters
            queryset = queryset.filter(q_non_living | q_living)

        return queryset.order_by("birth_year")

    def resolve_figure(self, info, id=None, name=None):
        if id:
            qs = Figure.objects.filter(pk=id)
        elif name:
            # Case-insensitive name lookup
            qs = Figure.objects.filter(name__iexact=name)
        else:
            return None

        # Optimization: Mitigate N+1 for relationships
        return (
            qs.prefetch_related("fields")
            .prefetch_related("influenced_by_set__influencer")
            .first()
        )