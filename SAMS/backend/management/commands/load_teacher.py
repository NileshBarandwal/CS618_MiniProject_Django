import csv
from django.core.management.base import BaseCommand
from backend.models import Teacher  # Replace 'your_app' with the actual name of your Django app

class Command(BaseCommand):
    help = 'Load teacher data from a CSV file into the Teacher table'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file to import teacher data from')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        # Open the CSV file and read it
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            teachers = [
                Teacher(
                    id=row['id'],
                    name=row['name'],
                    email=row['email']
                )
                for row in reader
            ]
            
            # Bulk create all Teacher records in the database
            Teacher.objects.bulk_create(teachers, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(teachers)} records into Teacher table'))
