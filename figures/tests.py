from django.test import TestCase
from .models import Figure, Field

class FigureModelTest(TestCase):
    def setUp(self):
        field = Field.objects.create(name="Science")
        self.figure = Figure.objects.create(
            name="Albert Einstein",
            slug="albert-einstein",
            wikidata_id="Q937",
            summary="Physicist",
            birth_date="1879-03-14",
            death_date="1955-04-18",
            normalized_birth_year=1879,
            normalized_death_year=1955,
            instance_of_QIDs=["Q5"]
        )
        self.figure.fields.add(field)

    def test_figure_creation(self):
        self.assertEqual(self.figure.name, "Albert Einstein")
        self.assertEqual(self.figure.slug, "albert-einstein")
        self.assertEqual(self.figure.wikidata_id, "Q937")
        self.assertEqual(self.figure.normalized_birth_year, 1879)
        self.assertEqual(self.figure.normalized_death_year, 1955)
        self.assertEqual(list(self.figure.instance_of_QIDs), ["Q5"])
        self.assertEqual(self.figure.fields.first().name, "Science")
