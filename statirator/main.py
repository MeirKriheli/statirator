import os
import sys


def main():
    # init is a special case, cause we want to add statirator.core to
    # INSTALLED_APPS, and have the command picked up. we'll handle it in here

    if 'init' in sys.argv:
        from django.conf import settings
        settings.configure(INSTALLED_APPS=('statirator.core', ))
    elif 'test' in sys.argv:
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "statirator.test_settings")

    from django.core import management
    management.execute_from_command_line()


if __name__ == '__main__':
    main()
