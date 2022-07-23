from django.core.management.base import BaseCommand
from store.models import OrderItem

class Command(BaseCommand):
    def handle(self, *args, **options):
        OrderItem.objects.all().delete()
        