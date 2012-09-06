import sys
import argparse
import logging
from . import commands


def create_options():
    "Add options to tornado"

    parser = argparse.ArgumentParser(
        'Staitrator - Static multilingual site and blog generator')

    log_level_choices = ['error', 'info', 'debug', 'none']
    parser.add_argument('--logging', choices=log_level_choices,
                        default='info',
                        help='Log level [Default: %(default)s]. "none" won\'t touch logging')

    sub_parsers = parser.add_subparsers(help='Sub Commands help')
    init = sub_parsers.add_parser('init', help='Initiate a new site')

    init.add_argument('directory', help='Target directory')
    init.add_argument('-n', '--name', default='Default site',
                      help='Site name and title [Default: %(default)s]')
    init.add_argument('-d', '--domain', default='example.com',
                      help='Domain name [Default: %(default)s]')
    init.add_argument('-b', '--build', default='build',
                      help="Site's build directory [Default: %(default)s]")
    init.add_argument(
        '-f', '--force', default=False, action='store_true',
        help='Ignore directory creation errors and '
        'overwrite site setting [Default: %(default)s]')
    init.add_argument(
        '-l', '--languages', nargs='*', dest='languages', default=['he', 'en'],
        help='Supported languages. [Default: %(default)s]')

    init.set_defaults(func=commands.init)

    generate = sub_parsers.add_parser('generate', help='Generate the site')
    generate.set_defaults(func=commands.generate)

    serve = sub_parsers.add_parser('serve', help='Serve the site, listening '
                                   'on a local port')
    serve.set_defaults(func=commands.serve)

    return parser


def setup_logging(args):
    if args.logging == 'none':
        return

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, args.logging.upper()))


def main():
    # init is a special case, cause we want to add statirator.core to
    # INSTALLED_APPS, and have the command picked up. we'll handle it in here

    if 'init' in sys.argv:
        from django.conf import settings
        settings.configure(INSTALLED_APPS=('statirator.core', ))

    from django.core import management
    management.execute_from_command_line()


if __name__ == '__main__':
    main()
