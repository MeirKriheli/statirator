from __future__ import print_function, absolute_import

import os
from django.conf import settings
from django.template import Template, RequestContext
from django.utils import translation
from django.test.client import RequestFactory

from statirator.core.utils import find_files, render_block_to_string
from .utils import get_pages_dir
from .models import Page


def update_post(slug, lang_code, defaults):
    with translation.override(lang_code):
        page, created = Page.objects.get_or_create(
            slug=slug,
            language=lang_code,
            defaults=defaults)

        if not created:
            for field, val in defaults.iteritems():
                setattr(page, field, val)
        # get the title from the template
        t = Template(page.content)
        req = RequestFactory().get(page.get_absolute_url(), LANGUAGE_CODE=lang_code)
        page.title = render_block_to_string(
            t, 'title', context_instance=RequestContext(req))
        page.description = render_block_to_string(
            t, 'description', context_instance=RequestContext(req))

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
                defaults = dict(content=template_content, page_type='html')
                update_post(slug, lang_code, defaults)


READERS = [html_reader]
