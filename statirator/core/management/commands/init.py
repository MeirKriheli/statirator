import os
from optparse import make_option
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Init the static site project"

    args = '[directory]'

    option_list = (
        make_option(
            '--title', '-t', dest='title', default='Default site',
            help='Site title [Default: "%defaults"]'),
        make_option(
            '--domain', '-d', dest='domain', default='example.com',
            help='Domain name [Default: "%default"]'),
        make_option(
            '--languages', '-l', dest='languages', default=['he', 'en'],
            action='append', help='Supported languages. [Default: "%default"]')
    ) + BaseCommand.option_list

    def handle(self, directory, **options):

        from django.conf.global_settings import LANGUAGES

        extra = {
            'build': 'build',
            'default_lang': options['languages'][0],
            'languages': [l for l in LANGUAGES if l[0] in options["languages"]],
            'extensions': ('py', ),
            'files': (),
            'template': os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    os.pardir, os.pardir, os.pardir, 'project_template')),
        }
        extra.update(options)

        from django.core.management import call_command
        call_command('startproject', 'conf', directory, **extra)
