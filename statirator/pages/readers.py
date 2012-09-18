from __future__ import print_function, absolute_import

import os
from django.conf import settings
from statirator.core.utils import find_files
from statirator.core.parsers import parse_rst
from .utils import get_pages_dir
from .models import Page


def rst_reader():
    "Finds rst pages, parses them and loads into the db."

    for page in find_files(get_pages_dir(), ['.rst']):
        print('Processing {0}'.format(page))
        with open(page) as p:
            parsed = parse_rst(p.read())

            generic_metadata, title, content = parsed.next()

            # got those, now go over the languages
            for metadata, title, content in parsed:
                lang = metadata['lang']

                page = Page(
                    title=title,
                    slug=generic_metadata['slug'],
                    content=content,
                    language=lang,
                    page_type='rst')
                page.save()


def html_reader():
    "Finds django html pages, parses them and loads into the db."

    for page in find_files(get_pages_dir(), ['.html']):
        print('Processing {0}'.format(page))
        slug, ext = os.path.splitext(os.path.basename(page))

        with open(page) as p:
            template_content = p.read()

            # we create one for each language. Less efficient, but will work we
            # i18n_permalink without further hacking
            #
            # Each template will be renderd for each language, so make sure to
            # have language logic in the template
            for lang_code, lang_name in settings.LANGUAGES:
                page = Page(
                    title=slug,
                    slug=slug,
                    content=template_content,
                    language=lang_code,
                    page_type='html')

                page.save()


READERS = [rst_reader, html_reader]
