from __future__ import print_function, absolute_import

import os
from django.conf import settings
from django.template import Template, RequestContext
from django.utils import translation
from django.test.client import RequestFactory

from statirator.core.utils import find_files, render_block_to_string
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

                translation.activate(lang_code)
                page = Page(
                    slug=slug,
                    content=template_content,
                    language=lang_code,
                    page_type='html')

                # get the title from the template
                t = Template(template_content)
                req = RequestFactory().get(page.get_absolute_url())
                page.title = render_block_to_string(
                    t, 'title', context_instance=RequestContext(req))

                page.save()


READERS = [rst_reader, html_reader]
