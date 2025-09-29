import graphene
from graphene_django.types import DjangoObjectType
from .models import Figure
from django.db import IntegrityError

# --- 1. Graphene Type Definition ---
class FigureType(DjangoObjectType):
    """Defines the structure of the Figure in GraphQL."""
    class Meta:
        model = Figure
        fields = ("id", "name", "birthYear", "deathYear", "description")

# --- 2. Query Definition ---
class FigureQuery(graphene.ObjectType):
    """Handles fetching Figure data."""
    figures = graphene.List(FigureType)
    
    def resolve_figures(root, info):
        """Resolver to fetch all Figure objects, ordered by birthYear."""
        return Figure.objects.all()

# --- 3. Mutation Input Definition ---
class FigureInput(graphene.InputObjectType):
    """Defines the structure of the input object for Figure mutations."""
    name = graphene.String(required=True)
    birthYear = graphene.Int(required=True)
    deathYear = graphene.Int(required=True)
    description = graphene.String(required=False)

# --- 4. Mutation Definition (Create Operation) ---
class CreateFigure(graphene.Mutation):
    """Mutation to create a new Figure."""
    # Output field is the created figure instance
    figure = graphene.Field(FigureType)

    class Arguments:
        # CRITICAL FIX: Defines a single 'input' argument using the InputObjectType
        input = FigureInput(required=True)

    @staticmethod
    def mutate(root, info, input=None):
        """The core logic for creating the figure."""
        try:
            figure = Figure.objects.create(
                name=input.name,
                birthYear=input.birthYear,
                deathYear=input.deathYear,
                description=input.description if input.description else ""
            )
            return CreateFigure(figure=figure)
        except IntegrityError as e:
            raise Exception(f"Database error while creating Figure: {e}")
        except Exception as e:
            # General catch-all for unexpected issues
            raise Exception(f"An unexpected error occurred: {e}")

# --- 5. Mutation Container ---
class FigureMutation(graphene.ObjectType):
    """Root container for all Figure-related mutations."""
    createFigure = CreateFigure.Field()