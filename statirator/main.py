import argparse
from . import commands

def create_options():
    "Add options to tornado"
    
    parser = argparse.ArgumentParser(
            'Staitrator - Static multilingual site and blog generator')

    sub_parsers = parser.add_subparsers(help='Sub Commands help')
    init = sub_parsers.add_parser('init', help='Initiate a new site')

    init.add_argument('directory', help='Target directory')
    init.add_argument('-n', '--name', default='Default site',
            help='Site name and title [default: %(default)s]')
    init.add_argument('-c', '--site_class', default='statirator.site.Html5Site',
            help='The base class for the site [default: %(default)s]')
    init.add_argument('-s', '--source', default='source',
            help="Site's source directory [default: %(default)s]")
    init.add_argument('-b', '--build', default='build',
            help="Site's build directory [default: %(default)s]")

    cmpl =  sub_parsers.add_parser('compile', help='Compile the new site')
    serve =  sub_parsers.add_parser('serve', help='Serve the site, listening '
            'on a local port')

    return parser

def main():
    parser = create_options()
    args = parser.parse_args()

    cmd = getattr(commands, args[0])
    cmd(args)

if __name__ == '__main__':
    main()
