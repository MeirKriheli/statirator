"""Handles cli arguments"""
import errno
import os
import sys

import logging


def init(args):
    """Create the initial site, populating code and templates"""

    #site = cls(name=args.name, root=args.directory,
    #        source=args.source, build=args.build,
    #        languages=args.languages)
    #site.create()
    logging.info("Initializing directory  %s", args.directory)

    # create the directories
    for folder in (args.source, args.build, 'conf', 'templates', 'static'):
        try:
            target = os.path.join(args.directory, folder)
            os.makedirs(target)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            if args.force:
                logging.debug('Target directory %s exists, continuing as force'
                              ' was set ', target)
            else:
                logging.error('Target directory %s already exist, aborting',
                              target)
                sys.exit(1)

    # template context
    from django.conf.global_settings import LANGUAGES

    ctx = {
        'source': args.source,
        'build': args.build,
        'default_lang': args.languages[0],
        'languages': [l for l in LANGUAGES if l[0] in args.languages],
    }

    from django.template import Context, Template
    from django.conf import settings

    settings.configure()
    print Template(SETTINGS_TEMPLATE).render(Context(ctx))


def _site_from_config():

    sys.path.append(os.path.abspath(os.getcwd()))
    from config import site

    return site


def generate(args):
    """generate the site.

    should be run from site's root (location of config.py)"""

    site = _site_from_config()
    site.generate()


def serve(args):
    """Serve the site"""

    logging.error('Not implemented')
    sys.exit(1)
