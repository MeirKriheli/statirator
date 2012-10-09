from __future__ import absolute_import

from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from .models import Post, I18NTag
from statirator.core.syndication import LanguageFeed
from statirator.core.utils import i18n_reverse, content_absolute_links


class PostsFeed(LanguageFeed):

    def title(self):
        return _("Recent posts")

    def link(self):
        return i18n_reverse(self.language_code, 'blog_archive')

    def items(self):
        return Post.objects.filter(
            language=self.language_code,
            is_published=True).order_by('-pubdate')[:10]

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.pubdate

    def item_description(self, item):
        return content_absolute_links(item.content)

    def item_categories(self, item):
        return item.tags.values_list('name', flat=True)


class TagFeed(LanguageFeed):

    def get_object(self, request, slug):
        return get_object_or_404(
            I18NTag, slug_no_locale=slug,
            language=request.LANGUAGE_CODE)

    def title(self, obj):
        return _('Posts tagged with %(tag_name)s') % {'tag_name': obj.name}

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
        return content_absolute_links(item.content)
