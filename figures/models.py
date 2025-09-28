from django.db import models

class Figure(models.Model):
    """
    Represents a historical figure, as required by the figures GraphQL schema.
    """
    name = models.CharField(max_length=255)
    
    # CRITICAL FIX: Add default=0. This resolves the recurring migration prompt.
    birthYear = models.IntegerField(db_column='birth_year', default=0) 
    
    deathYear = models.IntegerField(db_column='death_year', null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['birthYear']