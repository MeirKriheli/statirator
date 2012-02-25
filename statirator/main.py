import argparse
from . import commands

VALID_ARGS = ('init', 'compile', 'serve')

def create_options():
    "Add options to tornado"
    
    parser = argparse.ArgumentParser(
            'Staitrator - Static multilingual site and blog generator')

    parser.add_argument('command', choices=VALID_ARGS)
    init = parser.add_argument_group('Init Options')
    init.add_argument('-n', '--name', default='Default site',
            help='Site name and title')
    init.add_argument('-c', '--site_class', default='statirator.site.Html5Site',
            help='The base class for the site')
    init.add_argument('-s', '--source', default='source', help="Site's source directory")
    init.add_argument('-b', '--build', default='build', help="Site's build directory")

    return parser

def main():
    parser = create_options()
    args = parser.parse_args()

    cmd = getattr(commands, args[0])
    cmd(args)

if __name__ == '__main__':
    main()
