import random
from django.core.management.base import BaseCommand
from django.db import transaction
from timeline.models import Figure, Field, Influence

class Command(BaseCommand):
    help = "Loads initial MVP data for Chronos Atlas."

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("--- Starting Chronos Atlas MVP Data Load ---"))

        # 1. Create Fields
        field_names = ["Philosophy", "Science", "Art", "Literature", "Politics", "Mathematics", "Medicine"]
        fields = {}
        for name in field_names:
            field, created = Field.objects.get_or_create(name=name)
            fields[name] = field
            if created:
                self.stdout.write(f"  Created Field: {name}")

        # 2. Create Figures
        figure_data = [
            # Ancient Era (BCE)
            {"name": "Plato", "desc": "Classical Greek philosopher.", "birth": -428, "death": -348, "fields": ["Philosophy", "Mathematics"]},
            {"name": "Aristotle", "desc": "Polymath and student of Plato.", "birth": -384, "death": -322, "fields": ["Philosophy", "Science", "Politics"]},
            # Renaissance Era
            {"name": "Leonardo da Vinci", "desc": "Renaissance polymath.", "birth": 1452, "death": 1519, "fields": ["Art", "Science", "Medicine"]},
            {"name": "William Shakespeare", "desc": "Greatest writer in the English language.", "birth": 1564, "death": 1616, "fields": ["Literature", "Art"]},
            # Industrial Age
            {"name": "Ada Lovelace", "desc": "First computer programmer.", "birth": 1815, "death": 1852, "fields": ["Mathematics", "Science"]},
            # Modern Era
            {"name": "Marie Curie", "desc": "Pioneering research on radioactivity.", "birth": 1867, "death": 1934, "fields": ["Science", "Medicine"]},
            {"name": "Albert Einstein", "desc": "Theorist of relativity.", "birth": 1879, "death": 1955, "fields": ["Science", "Mathematics"]},
            # Contemporary Era (Living Figure)
            {"name": "Noam Chomsky", "desc": "Linguist, philosopher, and political activist.", "birth": 1928, "death": None, "fields": ["Philosophy", "Politics", "Literature"]},
        ]

        figure_objects = {}
        for data in figure_data:
            figure, created = Figure.objects.get_or_create(
                name=data["name"],
                defaults={
                    "description": data["desc"],
                    "birth_year": data["birth"],
                    "death_year": data["death"],
                }
            )
            figure_objects[data["name"]] = figure
            
            # Link Fields (M2M)
            figure.fields.set([fields[f] for f in data["fields"]])
            
            if created:
                self.stdout.write(f"  Created Figure: {data['name']}")

        # 3. Create Influence Relationships
        influence_links = [
            ("Plato", "Aristotle"),
            ("Aristotle", "Leonardo da Vinci"),
            ("Leonardo da Vinci", "Marie Curie"),
            ("Plato", "Albert Einstein"),
            ("Marie Curie", "Albert Einstein"),
            ("Aristotle", "William Shakespeare"),
            ("Ada Lovelace", "Albert Einstein"),
            ("Plato", "Noam Chomsky"),
        ]

        for influencer_name, influenced_name in influence_links:
            influencer = figure_objects[influencer_name]
            influenced = figure_objects[influenced_name]
            
            # Check if influence already exists to maintain idempotency
            _, created = Influence.objects.get_or_create(
                influencer=influencer,
                influenced=influenced,
            )
            if created:
                self.stdout.write(f"  Created Influence: {influencer_name} -> {influenced_name}")
        
        self.stdout.write(self.style.SUCCESS("--- MVP Data Load Complete. 8 Figures, 8 Influences Ready. ---"))