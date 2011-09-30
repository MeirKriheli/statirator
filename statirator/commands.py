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

    if os.path.exists(root_dir):
        show_error('{0} already exists, aborting'.format(root_dir),
                show_help=False)


    logging.info('Creating "%s" at %s', opts.name, root_dir)
    os.makedirs(root_dir)

    _CURR_DIR = os.path.abspath(os.path.dirname(__file__))

    logging.info("\tCreating config.py from template")

    loader = template.Loader(os.path.join(_CURR_DIR, 'templates'))
    config_tmpl = loader.load('site_config.py.tmpl')
    output = config_tmpl.generate(name=opts.name, source=opts.source,
            build=opts.build)
    with open(os.path.join(root_dir, 'config.py'), 'w') as config_file:
        config_file.write(output)

    # now create the site directories
    for target_dir in (opts.source, opts.build,
            os.path.join(opts.source, '_templates')):
        logging.info('\tCreating %s directory', target_dir)
        os.makedirs(os.path.join(root_dir, target_dir))

    show_error('Not implemented', show_help=False)

def compile(args, options):
    """Compile the site"""

    logging.error('Not implemented')
    sys.exit(1)

def serve(args, options):
    """Serve the site"""

    logging.error('Not implemented')
    sys.exit(1)
