from __future__ import absolute_import

from django.contrib.sitemaps import Sitemap
from django.conf import settings
from django.core.urlresolvers import reverse

from statirator.core.models import DummyTranslation
from .models import Post, I18NTag


class BlogSiteMap(Sitemap):

    def items(self):
        "Return the items starting with defualt language and it's index page"

        default = settings.LANGUAGE_CODE
        langs = [default] + [x[0] for x in settings.LANGUAGES if x[0] != default]

        items = []
        for lang in langs:
            for slug in ('blog_archive', 'blog_tags'):
                dummy = DummyTranslation(None, lang, slug, reverse(slug))
                items.append(dummy)
            items.extend(Post.objects.filter(language=lang, is_published=True))
            items.extend(I18NTag.objects.filter(language=lang))

        return items
