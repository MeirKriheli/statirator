from __future__ import absolute_import

from django.contrib.sitemaps import Sitemap
from django.conf import settings

from .models import Page


class PagesSiteMap(Sitemap):

    def items(self):
        "Return the items starting with defualt language and it's index page"

        default = settings.LANGUAGE_CODE
        langs = [default] + [x[0] for x in settings.LANGUAGES if x[0] != default]

        items = []
        for lang in langs:
            idx = Page.objects.get(slug='index', language=lang)

            items.append(idx)

            items.extend(Page.objects.filter(language=lang).exclude(slug='index'))

        return items
