from __future__ import absolute_import
from django.conf import settings
from django.contrib.syndication.views import Feed

from .models import Post


class PostsFeed(Feed):

    def get_feed(self, obj, request):
        "Override to get items per language"

        try:
            self.language_code = request.LANGUAGE_CODE  # store it for later
        except AttributeError:
            self.language_code = settings.LANGUAGE_CODE

        feed = super(PostsFeed, self).get_feed(obj, request)
        feed.feed['language'] = self.language_code

        return feed

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
