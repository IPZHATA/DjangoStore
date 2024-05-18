from decimal import Decimal

from django.core.management.base import BaseCommand
from order.models import DeliveryProvider


class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **options):
        # Add your code here to populate the database
        DeliveryProvider.objects.create(description="Some description 1",
                                        name="First Option",
                                        price=Decimal(100))
        DeliveryProvider.objects.create(description="Some description 2",
                                        name="Second Option",
                                        price=Decimal(120))
        self.stdout.write(self.style.SUCCESS('Database populated successfully'))
