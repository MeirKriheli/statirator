"Site definition"
from __future__ import absolute_import
from tornado import template, httpclient
from collections import defaultdict, deque
import logging
import shutil
import os

CONFIG_TEMPLATE = """# Generated by statirator.
from {{ import_path }} import {{ class_name }}
import os

SITE_OPTS = {
    'root': os.path.abspath(os.path.dirname(__file__)),
    'name': '{{name}}',
    'source': '{{source}}',  # relative to build or absolute
    'build': '{{ build }}',  # relative to build or absolute
    'languages': ['he', 'en'],  #  First language is default
}

site = {{ class_name }}(**SITE_OPTS)
"""

class Site(object):
    """Basic Site object, creates the config file and an empty source dir"""

    def __init__(self, name='Default', root='.', source='source', build='build',
            languages=None, prefix_default_lang=False,
            ignore_starting_with='_'):
        """Defines the basic site object"""

        self.name = name
        self.root = os.path.abspath(root)
        self.source = os.path.abspath(os.path.join(root, source))
        self.build = os.path.abspath(os.path.join(root, build))
        self.ignore_starting_with = ignore_starting_with
        self.languages = languages

        self.source_templates_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'templates'))

        self.db = None

    def create(self):
        """Create the initial site"""

        if os.path.exists(self.root):
            logging.error('{0} already exists, aborting'.format(self.root),
                    show_help=False)

        logging.info('Creating "%s" at %s', self.name, self.root)
        os.makedirs(self.root)

        logging.info("Creating config.py from template")
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
        logging.info("Creating source directory (%s)", self.source)
        os.makedirs(os.path.join(self.root, self.source))

    def walk_site(self):
        """Walks the site's source dir yielding assets"""

        to_ignore = self.ignore_starting_with

        for root, dirs, assets in os.walk(self.source):
            dirs[:] = [d for d in dirs if not d.startswith(to_ignore)]

            for asset in assets:
                if not asset.startswith(to_ignore):
                    yield os.path.relpath(root, self.source), asset

    def compile(self):
        """Compiles the site from source to build dir"""

        self.db = defaultdict(deque)
        for asset_dir, asset in self.walk_site():
            logging.debug('%s - %s', asset_dir, asset)


class Html5Site(Site):
    """Basic Html5 site . Create:

    - Basic _site.html template
    - Modernizr
    - normalize.css

    """

    NORMALIZE = 'https://raw.github.com/necolas/normalize.css/master/normalize.css'

    def create(self):
        """Extra create elements"""

        super(Html5Site, self).create()
        self.get_css()
        self.create_js()
        self.copy_templates()

    def get_css(self):
        "create the css dir, and download normalize"

        logging.info('Creating css directory')
        css_dir = os.path.join(self.root, self.source, 'css')

        os.makedirs(css_dir)

        logging.info('Getting normalize.css')

        http_client = httpclient.HTTPClient()
        try:
            response = http_client.fetch(self.NORMALIZE)
            with open(os.path.join(css_dir, 'normalize.css'), 'w') as css_file:
                css_file.write(response.body)
        except httpclient.HTTPError, e:
            logging.error("Error getting normalize.css: {0}".format(e))

    def create_js(self):
        """Create js and download modernizr"""

        logging.info('Creating js directory')
        js_dir = os.path.join(self.root, self.source, 'js')

        os.makedirs(js_dir)

        logging.info('Copying modernizr.js')
        modernizr = os.path.join(self.source_templates_dir, 'html5',
                'modernizr.js')
        shutil.copy(modernizr, js_dir)

    def copy_templates(self):
        """Create dir and copy initial html templates"""

        logging.info('Creating _templates dir and copying templates')
        target_dir = os.path.join(self.root, self.source, '_templates')
        os.makedirs(target_dir)

        source_dir = os.path.join(self.source_templates_dir, 'html5')

        shutil.copy(os.path.join(source_dir, 'site.html'), target_dir)
