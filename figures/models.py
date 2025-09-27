import datetime
from django.db import models

class Figure(models.Model):
    """Represents a historical person or figure."""
    name = models.CharField(max_length=255)
    birthYear = models.IntegerField(blank=True, null=True)
    deathYear = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        # Assumes you want the model name to match the expected schema field
        verbose_name_plural = "figures"