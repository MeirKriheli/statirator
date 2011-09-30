from tornado import options
import logging

VALID_ARGS = ('init', 'build', 'serve')

def main():
    args = options.parse_command_line()

    if not args or args[0] not in VALID_ARGS:
        valid_opts = ', '.join(VALID_ARGS)
        logging.error('Invalid option. Valid options are {0}'.format(valid_opts))
        options.print_help()

if __name__ == '__main__':
    main()
