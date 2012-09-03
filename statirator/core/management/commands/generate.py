import logging

from django.core.management.base import BaseCommand
from statirator.utils import find_walkers


class Command(BaseCommand):

    help = "Walk the resources, builds the db, and generates the static site"

    def handle(self, *args, **options):
        self.walkers = find_walkers()

    def walk(self):
        """Walk to walkers to populate the db"""

        for walker in self.walkers:
            logging.info('Walking %s', walker)
            walker()
