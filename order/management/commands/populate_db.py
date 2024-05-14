from decimal import Decimal

from django.core.management.base import BaseCommand
from order.models import DeliveryOption


class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **options):
        # Add your code here to populate the database
        DeliveryOption.objects.create(description="Some description 1",
                                      name="First Option",
                                      price=Decimal(100))
        DeliveryOption.objects.create(description="Some description 2",
                                      name="Second Option",
                                      price=Decimal(120))
        self.stdout.write(self.style.SUCCESS('Database populated successfully'))
