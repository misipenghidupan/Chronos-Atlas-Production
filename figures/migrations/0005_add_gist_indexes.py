# figures/migrations/0005_add_gist_indexes.py

from django.db import migrations

class Migration(migrations.Migration):
    # Keep this, it doesn't hurt.
    atomic = False 
    
    dependencies = [
        ('figures', '0004_enable_btree_gist'), 
    ]

    operations = [
    migrations.RunSQL(
        """
        CREATE INDEX IF NOT EXISTS figures_figure_birth_year_gist_idx
        ON figures_figure USING GIST (normalized_birth_year int4_ops);

        CREATE INDEX IF NOT EXISTS figures_figure_death_year_gist_idx
        ON figures_figure USING GIST (normalized_death_year int4_ops);

        CREATE INDEX IF NOT EXISTS figures_figure_lifespan_gist_idx
        ON figures_figure USING GIST (normalized_birth_year int4_ops, normalized_death_year int4_ops);
        """,
        reverse_sql="""
        DROP INDEX IF EXISTS figures_figure_birth_year_gist_idx;
        DROP INDEX IF EXISTS figures_figure_death_year_gist_idx;
        DROP INDEX IF EXISTS figures_figure_lifespan_gist_idx;
        """
    ),
]