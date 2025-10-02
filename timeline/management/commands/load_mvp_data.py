from django.core.management.base import BaseCommand
from django.db import transaction

# Figure and Field are in 'figures' app.
# Influence is in 'timeline' app.
from figures.models import Field, Figure
from timeline.models import Influence, TimelineEvent


class Command(BaseCommand):
    help = "Load sample timeline data for MVP demonstration and testing purposes."

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.SUCCESS("--- Starting Chronos Atlas MVP Data Load ---")
        )

        # 1. Clear existing data to ensure idempotency and clean runs
        Influence.objects.all().delete()
        TimelineEvent.objects.all().delete()
        Figure.objects.all().delete()
        Field.objects.all().delete()
        self.stdout.write(
            self.style.WARNING(
                "  Cleared existing Figure, Field, Event, and Influence data."
            )
        )

        # 2. Create Fields
        field_names = [
            "Philosophy",
            "Science",
            "Art",
            "Literature",
            "Politics",
            "Mathematics",
            "Medicine",
        ]
        fields = {}
        for name in field_names:
            field, created = Field.objects.get_or_create(
                name=name, slug=name.lower()
            )  # Added slug to Field
            fields[name] = field
            if created:
                self.stdout.write(f"  Created Field: {name}")

        # 3. Create Figures
        figure_data = [
            # Ancient Era (BCE)
            {
                "name": "Plato",
                "desc": "Classical Greek philosopher.",
                "birth": -428,
                "death": -348,
                "fields": ["Philosophy", "Mathematics"],
                "wikidata": "Q859",
            },
            {
                "name": "Aristotle",
                "desc": "Polymath and student of Plato.",
                "birth": -384,
                "death": -322,
                "fields": ["Philosophy", "Science", "Politics", "Medicine"],
                "wikidata": "Q868",
            },
            # Middle Ages/Renaissance
            {
                "name": "Leonardo da Vinci",
                "desc": "Renaissance polymath, painter, sculptor, architect, musician, scientist.",
                "birth": 1452,
                "death": 1519,
                "fields": ["Art", "Science", "Mathematics"],
                "wikidata": "Q762",
            },
            {
                "name": "William Shakespeare",
                "desc": "English poet, playwright, and actor.",
                "birth": 1564,
                "death": 1616,
                "fields": ["Literature", "Art"],
                "wikidata": "Q692",
            },
            # Modern Era
            {
                "name": "Marie Curie",
                "desc": "Pioneering physicist and chemist, first woman to win a Nobel Prize.",
                "birth": 1867,
                "death": 1934,
                "fields": ["Science", "Medicine"],
                "wikidata": "Q7186",
            },
            {
                "name": "Albert Einstein",
                "desc": "Theoretical physicist who developed the theory of relativity.",
                "birth": 1879,
                "death": 1955,
                "fields": ["Science", "Mathematics", "Philosophy"],
                "wikidata": "Q937",
            },
            {
                "name": "Ada Lovelace",
                "desc": "English mathematician and writer, often regarded as the first computer programmer.",
                "birth": 1815,
                "death": 1852,
                "fields": ["Mathematics", "Science"],
                "wikidata": "Q7259",
            },
            # Contemporary
            {
                "name": "Noam Chomsky",
                "desc": "American linguist, philosopher, and political activist.",
                "birth": 1928,
                "death": 2024,  # Use 2024 since he is currently alive in the real world
                "fields": [
                    "Linguistics",
                    "Philosophy",
                    "Politics",
                ],  # Linguistics is a Field that should be created or included
                "wikidata": "Q9049",
            },
        ]

        figure_objects = {}
        for data in figure_data:
            # Ensure slug is generated (important for unique index)
            slug_val = data["name"].lower().replace(" ", "-")
            wikidata_val = data.get("wikidata")

            figure, created = Figure.objects.get_or_create(
                slug=slug_val,
                defaults={
                    "name": data["name"],
                    "summary": data["desc"],
                    "normalized_birth_year": data["birth"],
                    "normalized_death_year": data["death"],
                    "wikidata_id": wikidata_val,
                },
            )
            figure_objects[data["name"]] = figure

            # Link Fields (M2M) - ensures the figure's field set matches the list
            # Note: We need to ensure all fields exist. "Linguistics" must be handled.
            figure_fields = []
            for field_name in data["fields"]:
                # Create Field on the fly if it doesn't exist (like 'Linguistics')
                field, _ = Field.objects.get_or_create(
                    name=field_name, slug=field_name.lower()
                )
                figure_fields.append(field)

            figure.fields.set(figure_fields)

            if created:
                self.stdout.write(f"  Created Figure: {data['name']}")

        # 4. Create Timeline Events
        event_data = [
            {
                "title": "Plato's Academy founded",
                "year": -387,
                "category": "Education",
                "description": "The founding of Plato's Academy marked a critical moment for Western philosophy.",
            },
            {
                "title": "Aristotle teaches Alexander the Great",
                "year": -343,
                "category": "Politics",
                "description": (
                    "Aristotle mentored the future conqueror, influencing his views "
                    "on governance and science."
                ),
            },
            {
                "title": "Gutenberg Bible printed",
                "year": 1455,
                "category": "Technology",
                "description": "The start of the printing revolution, rapidly spreading knowledge across Europe.",
            },
            {
                "title": "Da Vinci paints Mona Lisa",
                "year": 1503,
                "category": "Art",
                "description": "One of the world's most recognizable artworks is completed.",
            },
            {
                "title": "Shakespeare's First Folio published",
                "year": 1623,
                "category": "Literature",
                "description": "Collection of 36 of Shakespeare's plays, saving many from obscurity.",
            },
            {
                "title": "Curie wins first Nobel Prize",
                "year": 1903,
                "category": "Science",
                "description": (
                    "Marie Curie and her husband Pierre win the Nobel Prize in Physics "
                    "for their work on radioactivity."
                ),
            },
            {
                "title": "Einstein publishes General Relativity",
                "year": 1915,
                "category": "Science",
                "description": "Albert Einstein publishes his groundbreaking theory of General Relativity.",
            },
        ]

        for data in event_data:
            _, created = TimelineEvent.objects.get_or_create(
                title=data["title"],
                year=data["year"],
                category=data["category"],
                description=data["description"],
            )
            if created:
                self.stdout.write(f"  Created Event: {data['title']}")

        # 5. Create Influence Relationships
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
            try:
                influencer = figure_objects[influencer_name]
                influenced = figure_objects[influenced_name]
            except KeyError as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"  Skipping Influence link due to missing figure: {e}"
                    )
                )
                continue

            # Check if influence already exists to maintain idempotency
            _, created = Influence.objects.get_or_create(
                influencer=influencer,
                influenced=influenced,
            )
            if created:
                self.stdout.write(
                    f"  Created Influence: " f"{influencer_name} -> {influenced_name}"
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"--- MVP Data Load Complete. "
                f"{Figure.objects.count()} Figures, "
                f"{TimelineEvent.objects.count()} Events, "
                f"{Influence.objects.count()} Influences Ready. ---"
            )
        )
