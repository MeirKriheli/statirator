import os
import sys


def main():
    if 'test' in sys.argv:
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "statirator.test_settings")
    else:
        from django.conf import settings
        settings.configure(INSTALLED_APPS=('statirator.core', ))

    from django.core import management
    management.execute_from_command_line()


if __name__ == '__main__':
    main()
