from __future__ import absolute_import
from tornado import options
from . import commands
import logging
import sys

VALID_ARGS = ('init', 'compile', 'serve')

def create_options():
    "Add options to tornado"

    options.define('name', default='Default site', group='Init options',
        help='Site name and title')
    options.define('source', default='_source', group='Init options',
        help="Site's source directory")
    options.define('build', default='_build', group='Init options',
        help="Site's build directory")
    options.define('templates', default='_templates', group='Init options',
        help="Site's templates directory")

def main():
    create_options()
    args = options.parse_command_line()

    if not args or args[0] not in VALID_ARGS:
        valid_opts = ', '.join(VALID_ARGS)
        logging.error('Invalid option. Valid options are {0}'.format(valid_opts))
        options.print_help()
        sys.exit(1)

    cmd = getattr(commands, args[0])
    cmd(args, options)

    if args[0] == 'init' and len(args) != 2:
        logging.error('init takes a single argument: dir name')
        options.print_help()

if __name__ == '__main__':
    main()
