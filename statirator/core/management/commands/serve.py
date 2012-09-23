from optparse import make_option
from django.core.management.base import NoArgsCommand, BaseCommand


class Command(NoArgsCommand):

    help = "Build and serve the static site"

    option_list = (
        make_option('--port', '-p', dest='port', default=8000, type='int',
                    help='The port to listen [Default: %default]'),
        make_option('--auto-rebuild', '-r', dest='auto_rebuild',
                    action='store_true', help='Auto rebuild static site on '
                    'each modification'),
    ) + BaseCommand.option_list

    def handle_noargs(self, **options):
        pass
