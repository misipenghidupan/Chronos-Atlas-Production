from django.core.management.base import BaseCommand
from django.db import connection

from figures.models import Figure


class Command(BaseCommand):
    help = (
        "Verifies that the custom GiST indexes are being used for range queries "
        "by temporarily manipulating table statistics."
    )

    def handle(self, *args, **options):
        # We target the specific table name
        table_name = Figure._meta.db_table

        self.stdout.write(
            self.style.SUCCESS("--- Verifying GiST Index on 'Figure' model ---")
        )

        query_plan = ""

        with connection.cursor() as cursor:
            self.stdout.write(
                "\nTemporarily adjusting table statistics to simulate a "
                "large table..."
            )
            # Faking the row count to force PostgreSQL to prefer the index
            cursor.execute(
                f"UPDATE pg_class SET reltuples = 50000 WHERE relname = "
                f"'{table_name}';"
            )
            cursor.execute(f"ANALYZE {table_name};")
            self.stdout.write(
                self.style.NOTICE("Statistics updated. Running test query.")
            )
            # The test query, ordered to accurately mimic typical range queries
            queryset = Figure.objects.filter(
                normalized_birth_year__lte=1900,
                normalized_death_year__gte=1800,
            ).order_by("normalized_birth_year", "name")
            raw_sql, params = queryset.query.sql_with_params()

            self.stdout.write(
                "\nRunning EXPLAIN (ANALYZE, BUFFERS) on the following query:"
            )
            self.stdout.write(self.style.SQL_KEYWORD(raw_sql % params))
            cursor.execute("EXPLAIN (ANALYZE, BUFFERS) " + raw_sql, params)

            self.stdout.write("\n--- PostgreSQL Query Plan ---")
            query_plan = "\n".join(row[0] for row in cursor.fetchall())
            self.stdout.write(query_plan)
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            actual_count = cursor.fetchone()[0]
            self.stdout.write("\nReverting table statistics to actual count...")
            # Reverting the row count back to the original value
            cursor.execute(
                f"UPDATE pg_class SET reltuples = {actual_count} WHERE relname = "
                f"'{table_name}';"
            )
            cursor.execute(f"ANALYZE {table_name};")
            self.stdout.write(
                self.style.NOTICE(f"Reverted to actual row count: {actual_count}.")
            )

        if "figure_lifespan_gist_idx" in query_plan:
            self.stdout.write(
                self.style.SUCCESS(
                    "\n✅ SUCCESS: The query plan includes a scan on "
                    "'figure_lifespan_gist_idx'. The index is functional, "
                    "though it may not be used on small data sets."
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    "\n❌ ERROR: Even with boosted statistics, the query plan did NOT "
                    "use 'figure_lifespan_gist_idx'. You may need to verify the index "
                    "definition in your migration files."
                )
            )
        self.stdout.write(self.style.SUCCESS("\n--- Verification Complete ---\n"))
