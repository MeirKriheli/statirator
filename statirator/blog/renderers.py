from __future__ import absolute_import

from django.conf import settings
from django.utils.translation import activate
from django_medusa.renderers import StaticSiteRenderer

from statirator.core.utils import i18n_reverse
from .models import Post, I18NTag


class BlogRenderer(StaticSiteRenderer):

    def get_paths(self):

        paths = []
        for lang_code, lang_name in settings.LANGUAGES:
            # posts
            activate(lang_code)
            items = Post.objects.filter(
                is_published=True, language=lang_code).order_by('-pubdate')

            paths.extend([i.get_absolute_url() for i in items])

            paths.append(i18n_reverse(lang_code, 'blog_archive'))
            paths.append(i18n_reverse(lang_code, 'blog_feed'))

        return paths


class TagsRenderer(StaticSiteRenderer):

    def get_paths(self):

        paths = []
        for lang_code, lang_name in settings.LANGUAGES:
            activate(lang_code)
            items = list(
                I18NTag.objects.filter(language=lang_code).order_by('name'))

            paths.extend([i.get_absolute_url() for i in items])

            for tag in items:
                paths.append(i18n_reverse(lang_code, 'blog_tag_feed',
                             kwargs={'slug': tag.slug_no_locale}))

            paths.append(i18n_reverse(lang_code, 'blog_tags'))

        return paths


renderers = [BlogRenderer, TagsRenderer]
