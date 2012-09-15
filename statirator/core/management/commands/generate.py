from __future__ import print_function
import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand
from statirator.core.utils import find_readers


class Command(BaseCommand):

    help = "Walk the resources, builds the db, and generates the static site"

    def handle(self, *args, **options):

        self.syncdb()
        self.create_sites()
        self.read_resources()
        self.gen_static()
        self.collect_static_media()

    def print_title(self, title):
        print()
        print(title)
        print(len(title) * '-')

    def syncdb(self):
        self.print_title('Syncing in memory db')
        # make sure we have the db
        call_command('syncdb', load_initial_data=False, interactive=False)

    def create_sites(self):
        "Make sure we have the site framework setup correctly"
        from django.conf import settings
        from django.contrib.sites.models import Site

        Site.objects.all().delete()

        for idx, (domain, lang, title) in enumerate(settings.SITES, 1):
            site = Site(domain=domain, name=title, pk=idx)
            site.save()

    def read_resources(self):
        """Walk to readers to populate the db"""

        readers = find_readers()
        self.print_title('Reading resource')

        for reader in readers:
            logging.info('Reading with %s', reader)
            reader()

    def gen_static(self):
        self.print_title('Generating static pages')

        # Use django-medusa for static pages
        call_command('staticsitegen')

    def collect_static_media(self):
        self.print_title('Collecting static media')
        call_command('collectstatic', interactive=False)
