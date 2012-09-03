"""Handles cli arguments"""
import os
import sys
import logging


def init(args):
    """Create the initial site, populating code and templates"""

    #site = cls(name=args.name, root=args.directory,
    #        source=args.source, build=args.build,
    #        languages=args.languages)
    #site.create()
    logging.info("Initializing project structure in  %s", args.directory)

    os.makedirs(args.directory)

    # options context
    from django.conf.global_settings import LANGUAGES

    ctx = {
        'build': args.build,
        'default_lang': args.languages[0],
        'languages': [l for l in LANGUAGES if l[0] in args.languages],
        'verbosity': 1,
        'extensions': ('py', ),
        'files': (),
        'template': os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    'project_template'))
    }

    from django.core.management import call_command
    call_command('startproject', 'conf', args.directory, **ctx)


def generate(args):
    """generate the site.

    should be run from site's root (location of manage.py)"""

    site = _site_from_config()
    site.generate()


def serve(args):
    """Serve the site"""

    logging.error('Not implemented')
    sys.exit(1)
