"""Handles cli arguments"""
from tornado import template
import logging
import sys
import os

def _show_error(options, message, show_help=True, exit=True):
    """Helper to show error and exit"""

    logging.error(message)

    if show_help:
        options.print_help()

    if exit:
        sys.exit(1)

def init(args, options):
    """Create the initial site, populating code and templates"""

    if len(args) != 2:
        _show_error(options, 'init takes a single argument: dir name')

    root_dir = args[1]

    #if os.path.exists(root_dir):
    #    _show_error(options, '{0} already exists, aborting'.format(root_dir),
    #            show_help=False)

    #os.makedirs(root_dir)

    _CURR_DIR = os.path.abspath(os.path.dirname(__file__))
    _CONF_TEMPLATE = 'site_config.py'

    loader = template.Loader(os.path.join(_CURR_DIR, 'templates'))

    config_tmpl = loader.load('{0}.tmpl'.format(_CONF_TEMPLATE))
    opts = options.options
    output = config_tmpl.generate(name=opts.name, source=opts.source,
            build=opts.build, templates=opts.templates)
    with open(os.path.join(root_dir, _CONF_TEMPLATE), 'w') as config_file:
        config_file.write(output)

    _show_error(options, 'Not implemented', show_help=False)

def compile(args, options):
    """Compile the site"""

    logging.error('Not implemented')
    sys.exit(1)

def serve(args, options):
    """Serve the site"""

    logging.error('Not implemented')
    sys.exit(1)
