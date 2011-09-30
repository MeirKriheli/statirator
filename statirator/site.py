"Site definition"
from __future__ import absolute_import
from .errors import show_error
from tornado import template
import logging
import os

CONFIG_TEMPLATE = """# Generated by statirator.
from {{ import_path }} import {{ class_name }}
import os

SITE_OPTS = {
    'root': os.path.abspath(os.path.dirname(__file__)),
    'name': '{{name}}',
    'source': '{{source}}',
    'build': '{{ build }}',
}

site = {{ class_name }}(**SITE_OPTS)
"""

class Site(object):
    """Basic Site object, creates the config file and an empty source dir"""

    def __init__(self, name='Default', root='.', source='source', build='build',
            ignore_starting_with='_'):
        """Defines the basic site object"""

        self.name = name
        self.root = os.path.abspath(root)
        self.source = source
        self.build = build
        self.ignore_starting_with = ignore_starting_with

    def create(self):
        """Create the initial site"""

        if os.path.exists(self.root):
            show_error('{0} already exists, aborting'.format(self.root),
                    show_help=False)

        logging.info('Creating "%s" at %s', self.name, self.root)
        os.makedirs(self.root)

        logging.info("\tCreating config.py from template")
        config_t = template.Template(CONFIG_TEMPLATE, autoescape=None)
        config_filename = os.path.join(self.root, 'config.py')

        context = {
            'name': self.name,
            'source': self.source,
            'build': self.build,
            'import_path': self.__module__,
            'class_name': self.__class__.__name__,
        }

        with open(config_filename, 'w') as config_file:
            config_file.write(config_t.generate(**context))

        # create the source directory
        logging.info("\tCreating source directory (%s)", self.source)
        os.makedirs(os.path.join(self.root, self.source))

class Html5Site(Site):
    """Basic Html5 site"""
