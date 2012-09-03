from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Walk the resources, builds the db, and generates the static site"

    def handle(self, *args, **options):
        pass
