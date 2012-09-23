from __future__ import print_function, absolute_import
import os
import SocketServer
import BaseHTTPServer
import SimpleHTTPServer
from optparse import make_option
from django.core.management import call_command
from django.core.management.base import NoArgsCommand, BaseCommand
from django.conf import settings


class ThreadedHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    "Threaded basic http server"


class Command(NoArgsCommand):

    help = "Build and serve the static site"

    option_list = (
        make_option('--port', '-p', dest='port', default=8000, type='int',
                    help='The port to listen [Default: %default]'),
        make_option('--auto-rebuild', '-r', dest='rebuild',
                    action='store_true', help='Auto rebuild static site on '
                    'each modification'),
    ) + BaseCommand.option_list

    def handle_noargs(self, **options):

        # Genarate on first run
        self.generate()

        curr_dir = os.getcwd()
        try:
            os.chdir(settings.BUILD_DIR)
            self.serve(options['port'], options['rebuild'])
        finally:
            os.chdir(curr_dir)

    def generate(self):
        call_command('generate')

    def serve(self, port, rebuild):
        server = ThreadedHTTPServer(('', port), SimpleHTTPServer.SimpleHTTPRequestHandler)

        try:
            # TODO Handle auto rebuild
            server.serve_forever()
        except KeyboardInterrupt:
            print('Shutting down')
