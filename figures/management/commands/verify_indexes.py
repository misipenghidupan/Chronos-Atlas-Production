from django.core.management.base import BaseCommand
from django.db import connection

from figures.models import Figure


class Command(BaseCommand):
    help = "Verifies that the custom GiST indexes are being used for range queries."

    def handle(self, *args, **options):
        """
        Run a sample query with EXPLAIN ANALYZE to check
        if our GiST index is being used for range queries.
        """
        self.stdout.write(
            self.style.SUCCESS("--- Verifying GiST Index on 'Figure' model ---")
        )

        # This query finds figures whose lifespans overlap with
        # the 19th century. Perfect for testing our GiST index.
        queryset = Figure.objects.filter(
            normalized_birth_year__lte=1900,
            normalized_death_year__gte=1800,
        )

        # Get the raw SQL that Django generates for this query
        raw_sql, params = queryset.query.sql_with_params()

        self.stdout.write("\nRunning EXPLAIN ANALYZE on the following query:")
        self.stdout.write(self.style.SQL_KEYWORD(raw_sql % params))

        with connection.cursor() as cursor:
            # Prepend EXPLAIN to the query to get the execution plan
            cursor.execute("EXPLAIN (ANALYZE, BUFFERS) " + raw_sql, params)

            self.stdout.write("\n--- PostgreSQL Query Plan ---")
            query_plan = "\n".join(row[0] for row in cursor.fetchall())
            self.stdout.write(query_plan)

        # Check if the query plan includes a scan on our GiST index
        if "figure_lifespan_gist_idx" in query_plan:
            self.stdout.write(
                self.style.SUCCESS(
                    "\n✅ SUCCESS: The query plan includes a scan on "
                    "'figure_lifespan_gist_idx'."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "\n⚠️ WARNING: Query plan did NOT use "
                    "'figure_lifespan_gist_idx'. The database chose "
                    "a different execution plan."
                )
            )
