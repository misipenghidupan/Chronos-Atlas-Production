# figures/management/commands/load_figures.py

import csv
import os
from django.core.management.base import BaseCommand
from figures.models import Figure # Import your Figure model

# Define the expected path to your CSV file
# Adjust this path based on where you placed your data file in the Docker build context
CSV_FILE_PATH = os.path.join(os.getcwd(), 'data', 'historical_figures_normalized.csv') 

class Command(BaseCommand):
    help = 'Loads figure data from the normalized CSV file.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting figure data loading...'))
        
        # Ensure the file exists before proceeding
        if not os.path.exists(CSV_FILE_PATH):
            self.stderr.write(self.style.ERROR(f'CSV file not found at: {CSV_FILE_PATH}'))
            return

        with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            figures_to_create = []
            
            for row in reader:
                try:
                    # Construct the Figure object, converting year strings to integers
                    figure = Figure(
                        name=row['name'],
                        birth_year=int(row['birth_year']),
                        death_year=int(row['death_year']),
                        normalized_birth_year=int(row['normalized_birth_year']),
                        normalized_death_year=int(row['normalized_death_year']),
                        # Add other model fields here
                    )
                    figures_to_create.append(figure)
                except KeyError as e:
                    self.stderr.write(self.style.ERROR(f"Missing column in CSV: {e}"))
                    return
                except ValueError as e:
                    self.stderr.write(self.style.ERROR(f"Data type error in row: {row}. Error: {e}"))
                    return

            # Use bulk_create for massive performance gains
            Figure.objects.bulk_create(figures_to_create, ignore_conflicts=True)
            
            self.stdout.write(self.style.SUCCESS(
                f'Successfully loaded and created {len(figures_to_create)} figure records.'
            ))