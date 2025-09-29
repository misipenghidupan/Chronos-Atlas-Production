from django.db import models
from figures.models import Figure # REQUIRED for the Influence model

class TimelineEvent(models.Model):
    """
    Represents a single event to be displayed on the chronological timeline.
    """
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.year}: {self.title}"

    class Meta:
        ordering = ['year']

# CRITICAL: MISSING MODEL ADDED FOR data loading (load_mvp_data.py)
class Influence(models.Model):
    """
    A relationship model defining influence between two historical figures.
    """
    influencer = models.ForeignKey(
        Figure,
        on_delete=models.CASCADE,
        related_name='influences_given'
    )
    influenced = models.ForeignKey(
        Figure,
        on_delete=models.CASCADE,
        related_name='influences_received'
    )
    # Optional fields could be added here (e.g., degree of influence, source)
    
    class Meta:
        unique_together = ['influencer', 'influenced']
        verbose_name = "Influence Relationship"
        verbose_name_plural = "Influence Relationships"

    def __str__(self):
        return f"{self.influencer.name} influenced {self.influenced.name}"