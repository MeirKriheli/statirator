from __future__ import absolute_import
from django.conf import settings
from statirator.core.syndication import LanguageFeed

from .models import Post


class PostsFeed(LanguageFeed):

    def link(self):
        if self.language_code == settings.LANGUAGE_CODE:
            return '/'

        return '/{0}/'.format(self.language_code)

    def items(self):
        return Post.objects.filter(
            language=self.language_code,
            is_published=True).order_by('-pubdate')[:10]

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.pubdate

    def item_description(self, item):
        # TODO return item excerpt if exists
        return item.content

    def item_categories(self, item):
        return item.tags.values_list('name', flat=True)
