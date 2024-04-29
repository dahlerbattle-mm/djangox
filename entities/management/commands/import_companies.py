import csv
from django.core.management.base import BaseCommand
from entities.models import GlobalCompanies

class Command(BaseCommand):
    help = 'Import companies from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Extract data from the row
                gc_id = row['gc_id']
                name = row['name']
                url = row['url']
                city = row['city']
                state = row['state']
                country = row['country']
                size = row['size']
                sector = row['sector']
                image = row['image']

                # Create GlobalCompanies instance and save to the database
                global_company = GlobalCompanies.objects.create(
                    gc_id=gc_id,
                    name=name,
                    url=url,
                    city=city,
                    state=state,
                    country=country,
                    size=size,
                    sector=sector,
                    image=image
                )

                # Print confirmation message
                self.stdout.write(self.style.SUCCESS(f'Added company: {name}'))