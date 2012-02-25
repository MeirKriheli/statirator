"""Handles cli arguments"""
import logging
import sys
import os

def init(args):
    """Create the initial site, populating code and templates"""

    site_module, site_class = args.site_class.rsplit('.', 1)
    try:
        imported_module = __import__(site_module, globals(), locals(), [site_class])
    except ImportError as e:
        logging.error(str(e), show_help=False)

    try:
        cls = getattr(imported_module, site_class)
    except AttributeError as e:
        logging.error(str(e), show_help=False)

    site = cls(name=opts.name, root=args[1], source=opts.source, build=opts.build)
    site.create()

def _site_site_from_config():

    sys.path.append(os.path.abspath(os.getcwd()))
    from config import site

    return site

def generate(args):
    """generate the site.
    
    should be run from site's root (location of config.py)"""

    site = _site_site_from_config()
    site.compile()

def serve(args):
    """Serve the site"""

    logging.error('Not implemented')
    sys.exit(1)
