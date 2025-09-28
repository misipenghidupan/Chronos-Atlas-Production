# figures/migrations/0004_enable_btree_gist.py

from django.db import migrations
from django.contrib.postgres.operations import CreateExtension


class Migration(migrations.Migration):

    dependencies = [
        # This must depend on the last successful migration
        ('figures', '0003_alter_figure_slug_alter_figure_wikidata_id'), 
    ]

    operations = [
        # CRITICAL: This operation installs the required PostgreSQL extension
        # to allow GiST indexes on standard data types (like integers).
        CreateExtension('btree_gist'),
    ]