# figures/migrations/0002_add_core_fields.py
# (Rename the file you previously generated to this name)

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        # CRITICAL: This must point to the initial migration.
        ('figures', '0001_initial'),
    ]

    operations = [
        # This list should contain the operations that Django generated
        # based on your updated figures/models.py and your prompt answers.
        
        # 1. New Models (Field and Occupation)
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        
        # 2. Change Meta Options (ordering, verbose names)
        migrations.AlterModelOptions(
            name='figure',
            options={'ordering': ['normalized_birth_year', 'name'], 'verbose_name': 'Historical Figure', 'verbose_name_plural': 'Historical Figures'},
        ),
        
        # 3. Rename Field (description -> summary)
        migrations.RenameField(
            model_name='figure',
            old_name='description',
            new_name='summary',
        ),
        
        # 4. Remove Old Year Fields (assuming you had birthYear/deathYear)
        migrations.RemoveField(
            model_name='figure',
            name='birthYear',
        ),
        migrations.RemoveField(
            model_name='figure',
            name='deathYear',
        ),
        
        # 5. Add New Date/Field Columns (The core changes needed for ETL)
        migrations.AddField(
            model_name='figure',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='figure',
            name='death_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='figure',
            name='instance_of_QIDs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='figure',
            name='normalized_birth_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='figure',
            name='normalized_death_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        
        # 6. Add Required Non-Nullable Fields (with one-off defaults)
        migrations.AddField(
            model_name='figure',
            name='slug',
            field=models.SlugField(default='temp-slug', max_length=255, unique=True),
        ),
        # NOTE: You MUST manually remove the `default='temp-slug'` from your 
        # local figures/models.py file AFTER this migration is applied!
        
        migrations.AddField(
            model_name='figure',
            name='wikidata_id',
            field=models.CharField(default='temp-wikidata', max_length=50, unique=True),
        ),
        # NOTE: You MUST manually remove the `default='temp-wikidata'` from your
        # local figures/models.py file AFTER this migration is applied!

        # Assuming the removal operations for the GiST indexes were not needed here,
        # as they were part of the conflicting 0003. We skip them to keep 0002 clean.
    ]