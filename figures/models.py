# CORRECTED: RangeField must be imported from django.contrib.postgres.fields
from django.contrib.postgres.fields import RangeField
from django.contrib.postgres.indexes import GistIndex
from django.db import models
from django.db.models import F, Func


# New Model: Added to fix the ImportError: cannot import name 'Field'
class Field(models.Model):
    """
    Represents a field of study or category (e.g., Philosophy, Science, Art).
    Used to categorize figures.
    """

    name = models.CharField(max_length=100, unique=True)
    # FIX: Added default='placeholder-slug' to satisfy makemigrations
    # when adding a non-nullable field to an existing project.
    slug = models.SlugField(max_length=100, unique=True, default="placeholder-slug")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Field of Endeavor"
        verbose_name_plural = "Fields of Endeavor"


class Figure(models.Model):
    """
    Represents a historical figure.
    """

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    wikidata_id = models.CharField(max_length=50, unique=True)
    summary = models.TextField(blank=True, null=True)

    # Year fields
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    normalized_birth_year = models.IntegerField(db_index=True)
    normalized_death_year = models.IntegerField(db_index=True)

    # New Foreign Key: Added to link figures to a field of endeavor
    field = models.ForeignKey(
        Field, on_delete=models.SET_NULL, related_name="figures", null=True, blank=True
    )

    def __str__(self):
        # Updated for better representation
        return (
            f"{self.name} ({self.normalized_birth_year}-{self.normalized_death_year})"
        )

    fields = models.ManyToManyField("Field", related_name="figures_set")

    class Meta:
        verbose_name = "Figure"
        verbose_name_plural = "Figures"
        db_table = "figures_figure"

        # Define constraints for data integrity
        constraints = [
            # 1. Ensures birth year is always less than or equal to death year.
            models.CheckConstraint(
                check=models.Q(
                    normalized_birth_year__lte=models.F("normalized_death_year")
                ),
                name="birth_before_death",
            ),
            # 2. Ensures no two figures have the exact same lifespan span.
            models.UniqueConstraint(
                fields=["normalized_birth_year", "normalized_death_year"],
                name="unique_lifespan",
            ),
        ]

        # Define the custom GiST index for range queries (lifespan overlap)
        indexes = [
            # FIX: Removed 'fields=[]' and 'expressions=' keyword to comply with Django's GistIndex structure.
            # The Func object is passed as the first positional argument.
            GistIndex(
                Func(
                    F("normalized_birth_year"),
                    F("normalized_death_year"),
                    function="int4range",
                    output_field=RangeField,
                ),
                name="figure_lifespan_gist_idx",
            ),
            # Standard indexes
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
        ]

    ordering = ["normalized_birth_year", "name"]
