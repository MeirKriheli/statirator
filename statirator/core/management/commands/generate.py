from django.core.management.base import BaseCommand
from statirator.utils import find_walkers


class Command(BaseCommand):

    help = "Walk the resources, builds the db, and generates the static site"

    def handle(self, *args, **options):
        walkers = find_walkers()

        print walkers
