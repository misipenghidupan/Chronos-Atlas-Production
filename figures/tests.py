from django.test import TestCase
import json
from graphene_django.utils.testing import GraphQLTestCase
from .models import Figure, Field
from ChronosAtlas.schema import schema

class FigureGraphQLTests(GraphQLTestCase):
    """
    Test suite for the GraphQL schema related to the Figure model,
    covering both queries and mutations.
    """
    # Point to the root schema of your project
    GRAPHQL_SCHEMA = schema

    @classmethod
    def setUpTestData(cls):
        """
        Create non-modified objects for all test methods in this class.
        This method is run once, creating a clean set of data for the tests.
        """
        Figure.objects.create(
            name="Test Figure Alpha",
            slug="test-figure-alpha",
            wikidata_id="Q1",
            normalized_birth_year=1900,
            normalized_death_year=1980,
            summary="A test figure for GraphQL."
        )
        Figure.objects.create(
            name="Test Figure Beta",
            slug="test-figure-beta",
            wikidata_id="Q2",
            normalized_birth_year=1920,
            normalized_death_year=2000,
            summary="Another test figure."
        )

    def test_all_figures_query(self):
        """
        Tests the 'allFigures' query to ensure it returns all created figures.
        """
        response = self.query(
            """
            query {
              allFigures(first: 2) {
                edges {
                  node {
                    name
                    normalizedBirthYear
                  }
                }
              }
            }
            """
        )

        # Check that the response is successful
        self.assertResponseNoErrors(response)

        # Parse the response content
        content = json.loads(response.content)
        data = content['data']['allFigures']['edges']

        # Assert that the correct number of figures are returned
        self.assertEqual(len(data), 2)

        # Assert that the data matches what we created in setUpTestData
        self.assertEqual(data[0]['node']['name'], 'Test Figure Alpha')
        self.assertEqual(data[1]['node']['name'], 'Test Figure Beta')

    def test_create_figure_mutation(self):
        """
        Tests the 'createFigure' mutation to ensure a new figure can be created.
        """
        # 1. Define the mutation and variables
        mutation = """
            mutation createFigure($input: FigureInput!) {
              createFigure(input: $input) {
                figure {
                  id
                  name
                  normalizedBirthYear
                }
              }
            }
        """
        variables = {
            "input": {
                "name": "Test Figure Gamma",
                "slug": "test-figure-gamma",
                "wikidataId": "Q3",
                "normalizedBirthYear": 1950,
                "normalizedDeathYear": 2020,
                "summary": "A figure created via mutation."
            }
        }

        # 2. Execute the mutation
        response = self.query(mutation, input_data=variables["input"])

        # 3. Assert the response is successful and contains the new figure's data
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        data = content['data']['createFigure']['figure']
        self.assertEqual(data['name'], "Test Figure Gamma")
        self.assertEqual(data['normalizedBirthYear'], 1950)

        # 4. Verify the object was actually created in the database
        self.assertEqual(Figure.objects.count(), 3)
        new_figure = Figure.objects.get(name="Test Figure Gamma")
        self.assertIsNotNone(new_figure)
        self.assertEqual(new_figure.wikidata_id, "Q3")
