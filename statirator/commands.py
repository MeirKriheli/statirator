"""Handles cli arguments"""
from __future__ import absolute_import
from .errors import show_error
from tornado import template
import logging
import sys
import os

def init(args, options):
    """Create the initial site, populating code and templates"""

    if len(args) != 2:
        show_error('init takes a single argument: dir name')

    opts = options.options

    site_module, site_class = opts.site_class.rsplit('.', 1)
    try:
        imported_module = __import__(site_module, globals(), locals(), [site_class])
    except ImportError, e:
        show_error(str(e), show_help=False)

    try:
        cls = getattr(imported_module, site_class)
    except AttributeError, e:
        show_error(str(e), show_help=False)

    site = cls(name=opts.name, root=args[1], source=opts.source, build=opts.build)
    site.create()

def compile(args, options):
    """Compile the site"""

    logging.error('Not implemented')
    sys.exit(1)

def serve(args, options):
    """Serve the site"""

    logging.error('Not implemented')
    sys.exit(1)
