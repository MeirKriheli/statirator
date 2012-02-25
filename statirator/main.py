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

    init.set_defaults(func=commands.init)

    generate =  sub_parsers.add_parser('generate', help='Generate the site')
    generate.set_defaults(func=commands.generate)

    serve =  sub_parsers.add_parser('serve', help='Serve the site, listening '
            'on a local port')
    serve.set_defaults(func=commands.serve)

    return parser

def main():
    parser = create_options()
    args = parser.parse_args()

    args.func(args)

if __name__ == '__main__':
    main()
