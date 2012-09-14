from __future__ import print_function
import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand
from statirator.core.utils import find_readers


class Command(BaseCommand):

    help = "Walk the resources, builds the db, and generates the static site"

    def handle(self, *args, **options):

        print("Syncing in memory db\n" + 20 * '-')
        # make sure we have the db
        call_command('syncdb', load_initial_data=False, interactive=False)

        # load resources
        self.readers = find_readers()
        self.read_resources()

        print("\nGenerating static pages\n" + 22 * '-')

        # Use django-medusa for static pages
        call_command('staticsitegen')

        print("\nCollecting static media\n" + 23 * '-')
        call_command('collectstatic', interactive=False)

    def read_resources(self):
        """Walk to readers to populate the db"""

        for reader in self.readers:
            logging.info('Reading with %s', reader)
            reader()
