from django.db import models

class Field(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Figure(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    birth_year = models.IntegerField(help_text="Year of birth (use negative for BCE)")
    death_year = models.IntegerField(
        null=True, blank=True, help_text="Year of death (null if still alive)"
    )
    fields = models.ManyToManyField(Field)

    def __str__(self):
        return self.name

class Influence(models.Model):
    influencer = models.ForeignKey(
        Figure,
        on_delete=models.CASCADE,
        related_name="influences_set",  # People they influenced
    )
    influenced = models.ForeignKey(
        Figure,
        on_delete=models.CASCADE,
        related_name="influenced_by_set",  # People who influenced them
    )

    class Meta:
        # Ensures a figure cannot influence another figure multiple times
        unique_together = ("influencer", "influenced")

    def __str__(self):
        return f"{self.influencer.name} influenced {self.influenced.name}"