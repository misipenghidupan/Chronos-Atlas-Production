from django.db import models
from django.contrib.postgres.fields import ArrayField
# NOTE: GistIndex is imported here but we will add it via migration 0003, 
# not in the model's Meta class.

class Figure(models.Model):
    """
    Core entity representing a historical figure.
    Includes time-series fields (normalized_year) for performance.
    """
    # Core Data Fields
    name = models.CharField(max_length=255)
    
    # CRITICAL: Non-nullable fields
    slug = models.SlugField(unique=True, max_length=255)
    wikidata_id = models.CharField(max_length=50, unique=True)
    
    # Renamed field from 'description'
    summary = models.TextField(null=True, blank=True)
    
    # Date Fields
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    
    # CRITICAL: Indexed Integer Fields for Timeline Queries (Milestone 0.2 focus)
    normalized_birth_year = models.IntegerField(null=True, blank=True)
    normalized_death_year = models.IntegerField(null=True, blank=True)
    
    # Taxonomy and Filtering Fields
    instance_of_QIDs = models.JSONField(default=list, blank=True)
    
    # CRITICAL ADDITION: ManyToMany field needed by load_mvp_data.py
    fields = models.ManyToManyField('Field', related_name='figures')

    class Meta:
        verbose_name = "Historical Figure"
        verbose_name_plural = "Historical Figures"
        ordering = ['normalized_birth_year', 'name']
        # The GiST indexes are applied via the 0003 migration file.

    def __str__(self):
        return self.name

# Placeholder models for relationships (created in migration 0002)
class Field(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Occupation(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name