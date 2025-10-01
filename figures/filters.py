import django_filters

from .models import Figure


class FigureFilter(django_filters.FilterSet):
    """
    FilterSet for the Figure model to enable filtering by name and
    birth year range.
    """

    # Add a filter for the 'name' field with case-insensitive
    # containment lookup
    name = django_filters.CharFilter(lookup_expr="icontains")

    # Add filters for birth year range
    min_birth_year = django_filters.NumberFilter(
        field_name="normalized_birth_year",
        lookup_expr="gte",
    )
    max_birth_year = django_filters.NumberFilter(
        field_name="normalized_birth_year",
        lookup_expr="lte",
    )

    # Add an ordering filter to allow sorting by name and birth year.
    # The 'fields' argument is a tuple of (model_field_name, api_field_name).
    order_by = django_filters.OrderingFilter(
        fields=(
            ("name", "name"),
            ("normalized_birth_year", "birthYear"),
        ),
    )

    class Meta:
        model = Figure
        # Define fields that can be used for exact matching
        # in addition to the custom ones above
        fields = ["slug", "wikidata_id"]
