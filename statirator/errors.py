"""Error handling functionality"""

from tornado import options
import logging
import sys

def show_error(message, show_help=True, exit=True):
    """Helper to show error and exit"""

    logging.error(message)

    if show_help:
        options.print_help()

    if exit:
        sys.exit(1)
