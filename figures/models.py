from django.db import models

class Figure(models.Model):
    """
    Represents a historical figure, as required by the figures GraphQL schema.
    """
    name = models.CharField(max_length=255)
    # Using db_column to maintain Python naming conventions while allowing snake_case in the database
    birthYear = models.IntegerField(db_column='birth_year') 
    deathYear = models.IntegerField(db_column='death_year', null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['birthYear']