from __future__ import print_function

import os
import sys

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
            '--languages', '-l', dest='languages', default='he,en',
            help='Supported languages. [Default: "%default"]'),
        make_option(
            '--timezone', '-z', dest='timezone', default='America/Chicago',
            help='Time Zone. [Default: "%default"]'),
    ) + BaseCommand.option_list

    def handle(self, *args, **options):

        if len(args) != 1:
            raise CommandError('init takes one argument: directory name')

        directory = args[0]

        from django.conf.global_settings import LANGUAGES

        the_langs = dict(LANGUAGES)

        langs = options.pop('languages').split(',')

        # we need to keep ordering, for the default language
        try:
            languages = [(l, the_langs[l]) for l in langs]
        except KeyError, e:
            print("Invalid language specified:", e, end=". ")
            print("Valid languages are:")
            for name, desc in LANGUAGES:
                print(name, '(' + desc + ')')
            sys.exit(1)

        os.makedirs(directory)
        print("Initializing project structure in", directory)

        extra = {
            'build': 'build',
            'default_lang': langs[0],
            'languages': languages,
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

        print("\n\tdomain:", options['domain'])
        print("\ttimezone:", options['timezone'])
        print("\ttitle:", options['title'])
        print("\tlanguages:", ', '.join(langs))
