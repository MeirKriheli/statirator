import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand
from statirator.core.utils import find_readers


class Command(BaseCommand):

    help = "Walk the resources, builds the db, and generates the static site"

    def handle(self, *args, **options):

        # make sure we have the db
        call_command('syncdb')
        self.readers = find_readers()
        self.read_resources()

    def read_resources(self):
        """Walk to readers to populate the db"""

        for reader in self.readers:
            logging.info('Reading with %s', reader)
            reader()
