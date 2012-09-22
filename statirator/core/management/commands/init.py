import os
import logging
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option


class Command(BaseCommand):

    help = "Init the static site project"

    args = '[directory]'

    option_list = (
        make_option(
            '--title', '-t', dest='title', default='Default site',
            help='Site title [Default: "%default"]'),
        make_option(
            '--domain', '-d', dest='domain', default='example.com',
            help='Domain name [Default: "%default"]'),
        make_option(
            '--languages', '-l', dest='languages', default=['he', 'en'],
            action='append', help='Supported languages. [Default: "%default"]'),
        make_option(
            '--timezone', '-z', dest='timezone', default='America/Chicago',
            action='append', help='Time Zone. [Default: "%default"]'),
    ) + BaseCommand.option_list

    def handle(self, *args, **options):

        if len(args) != 1:
            raise CommandError('init takes one argument: directory name')

        directory = args[0]

        logging.info("Initializing project structure in  %s", directory)
        os.makedirs(directory)

        from django.conf.global_settings import LANGUAGES
        langs = options.pop('languages')

        extra = {
            'build': 'build',
            'default_lang': langs[0],
            'languages': [l for l in LANGUAGES if l[0] in langs],
            'extensions': ('py', ),
            'domain': options['domain'],
            'timezone': options['timezone'],
            'title': options['title'],
            'files': (),
            'template': os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    os.pardir, os.pardir, os.pardir, 'project_template')),
        }
        extra.update(options)

        from django.core.management import call_command
        call_command('startproject', 'conf', directory, **extra)
