from __future__ import print_function, absolute_import

import os
import time
import threading

import BaseHTTPServer
import SimpleHTTPServer
import SocketServer
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import NoArgsCommand, BaseCommand
from optparse import make_option

from statirator.core.utils import filesystem_changed


class ThreadedHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    "Threaded basic http server"


class Command(NoArgsCommand):

    help = "Build and serve the static site"

    option_list = (
        make_option('--port', '-p', dest='port', default=8000, type='int',
                    help='The port to listen [Default: %default]'),
        make_option('--auto-generate', '-g', dest='generate',
                    action='store_true', help='Auto generate static site on '
                    'each modification'),
    ) + BaseCommand.option_list

    def handle_noargs(self, **options):

        self.httpd_thread = None
        self.httpd_server = None
        self._shutdown = False
        curr_dir = os.getcwd()

        try:
            if options['generate']:
                self.filesystem_watcher()
            else:
                call_command('generate')

            os.chdir(settings.BUILD_DIR)
            self.serve(options['port'])

            while not self._shutdown:
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    self.shutdown()
        finally:
            os.chdir(curr_dir)

    def shutdown(self):
        print("\nShutting down")
        self._shutdown = True
        self.httpd_server.shutdown()
        self.httpd_thread.join()

    def filesystem_watcher(self):
        lock = threading.Lock()

        def watch():
            while not self._shutdown:
                with lock:
                    if filesystem_changed(settings.ROOT_DIR, ignore_dirs=[settings.BUILD_DIR]):
                        call_command('generate')
                    time.sleep(1)

        watcher_thread = threading.Thread(target=watch)
        watcher_thread.start()

    def serve(self, port):
        self.httpd_server = ThreadedHTTPServer(
            ('', port), SimpleHTTPServer.SimpleHTTPRequestHandler)

        self.httpd_thread = threading.Thread(target=self.httpd_server.serve_forever)
        self.httpd_thread.setDaemon(True)
        self.httpd_thread.start()
