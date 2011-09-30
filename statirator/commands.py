"""Handles cli arguments"""
import logging
import sys
import os

def init(args, options):
    """Create the initial site"""

    if len(args) != 2:
        logging.error('init takes a single argument: dir name')
        options.print_help()
        sys.exit(1)

    root_dir = args[1]

    if os.path.exists(root_dir):
        logging.error('{0} already exists, aborting'.format(root_dir))
        sys.exit(1)

    logging.error('Not implemented')
    sys.exit(1)

def compile(args, options):
    """Compile the site"""

    logging.error('Not implemented')
    sys.exit(1)

def serve(args, options):
    """Serve the site"""

    logging.error('Not implemented')
    sys.exit(1)
