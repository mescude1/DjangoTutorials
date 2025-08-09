from django.core.management.base import BaseCommand
from pages.factories import ProductFactory

class Command(BaseCommand):
    help = 'Seeds the database with new products'


    def handle(self, *args, **options):
        ProductFactory.create_batch(8)
        self.stdout.write(self.style.SUCCESS('Successfully seeded 8 products'))