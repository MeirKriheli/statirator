from __future__ import absolute_import

from django.conf import settings
from django.utils.translation import activate
from django.core.urlresolvers import reverse
from django_medusa.renderers import StaticSiteRenderer

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

            # archive and rss
            if lang_code == settings.LANGUAGE_CODE:
                paths.append(reverse('blog_archive'))
                paths.append(reverse('blog_feed'))
            else:
                paths.append(reverse('i18n_blog_archive'))
                paths.append(reverse('i18n_blog_feed'))

        return paths


class TagsRenderer(StaticSiteRenderer):

    def get_paths(self):

        paths = []
        for lang_code, lang_name in settings.LANGUAGES:
            activate(lang_code)
            items = I18NTag.objects.filter(language=lang_code).order_by('name')

            paths.extend([i.get_absolute_url() for i in items])

        return paths


renderers = [BlogRenderer, TagsRenderer]
