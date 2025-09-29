from django.test import TestCase
from .models import TimelineEvent, Influence
from figures.models import Figure

class TimelineEventModelTest(TestCase):
    def setUp(self):
        self.event = TimelineEvent.objects.create(
            title="Moon Landing",
            year=1969,
            category="Space",
            description="Apollo 11 landed on the moon."
        )

    def test_event_creation(self):
        self.assertEqual(self.event.title, "Moon Landing")
        self.assertEqual(self.event.year, 1969)
        self.assertEqual(self.event.category, "Space")

class InfluenceModelTest(TestCase):
    def setUp(self):
        self.influencer = Figure.objects.create(
            name="Isaac Newton",
            slug="isaac-newton",
            wikidata_id="Q935",
            normalized_birth_year=1643,
            normalized_death_year=1727,
            instance_of_QIDs=["Q5"]
        )
        self.influenced = Figure.objects.create(
            name="Albert Einstein",
            slug="albert-einstein",
            wikidata_id="Q937",
            normalized_birth_year=1879,
            normalized_death_year=1955,
            instance_of_QIDs=["Q5"]
        )
        self.influence = Influence.objects.create(
            influencer=self.influencer,
            influenced=self.influenced
        )

    def test_influence_creation(self):
        self.assertEqual(self.influence.influencer.name, "Isaac Newton")
        self.assertEqual(self.influence.influenced.name, "Albert Einstein")
