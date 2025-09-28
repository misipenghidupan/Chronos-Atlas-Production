import random
from django.core.management.base import BaseCommand
from django.db import transaction

# CORRECTED IMPORTS: 
# Figure and Field are in the 'figures' app. Influence is in the 'timeline' app.
from figures.models import Figure, Field 
from timeline.models import Influence 

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
            # Generate temporary unique IDs for required fields
            slug_val = data["name"].lower().replace(' ', '-')
            wikidata_val = f"Q-{data['name'].replace(' ', '')}-{abs(data['birth'])}"

            figure, created = Figure.objects.get_or_create(
                # Lookup is by name
                name=data["name"],
                defaults={
                    # Mapped data keys to Figure model fields
                    "summary": data["desc"],
                    "normalized_birth_year": data["birth"],
                    "normalized_death_year": data["death"],
                    
                    # Temporarily fill required unique fields
                    "slug": slug_val,
                    "wikidata_id": wikidata_val,
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