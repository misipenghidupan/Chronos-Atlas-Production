import django_filters
from .models import TimelineEvent

class TimelineEventFilter(django_filters.FilterSet):
    """
    FilterSet for the TimelineEvent model to enable filtering by year range and category.
    """
    # Add filters for year range
    min_year = django_filters.NumberFilter(field_name='year', lookup_expr='gte')
    max_year = django_filters.NumberFilter(field_name='year', lookup_expr='lte')

    # Add an ordering filter to allow sorting by year.
    order_by = django_filters.OrderingFilter(
        fields=(
            ('year', 'year'),
        )
    )

    class Meta:
        model = TimelineEvent
        # Allow exact matching on 'category' and 'year'
        fields = ['category', 'year']