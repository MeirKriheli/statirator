from __future__ import absolute_import
from django.conf import settings
from django.shortcuts import get_object_or_404

from statirator.core.syndication import LanguageFeed
from .models import Post, I18NTag


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


class TagFeed(LanguageFeed):

    def get_object(self, request, slug):
        return get_object_or_404(
            I18NTag, slug_no_locale=slug,
            language=request.LANGUAGE_CODE)

    def items(self, obj):
        return Post.objects.filter(
            language=obj.language,
            is_published=True,
            tags__slug__in=[obj.slug]).order_by('-pubdate')

    def link(self, obj):
        return obj.get_absolute_url()

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.pubdate

    def item_description(self, item):
        # TODO return item excerpt if exists
        return item.content
