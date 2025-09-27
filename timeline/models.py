from django.db import models

class TimelineEvent(models.Model):
    """
    Represents a single event to be displayed on the chronological timeline.
    This model is required by the Graphene schema definition in timeline/schema.py.
    """
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.year}: {self.title}"

    class Meta:
        ordering = ['year']
