from __future__ import absolute_import

from django.conf import settings
from django.utils.translation import activate
from django.core.urlresolvers import reverse
from django_medusa.renderers import StaticSiteRenderer

from .models import Post


class BlogRenderer(StaticSiteRenderer):

    def get_paths(self):

        paths = []
        for lang_code, lang_name in settings.LANGUAGES:
            # posts
            activate(lang_code)
            items = Post.objects.filter(
                is_published=True, language=lang_code).order_by('-pubdate')

            paths.extend([i.get_absolute_url() for i in items])

            # archive
            if lang_code == settings.LANGUAGE_CODE:
                paths.append(reverse('blog_archive'))
            else:
                paths.append(reverse('i18n_blog_archive'))

        return paths

renderers = [BlogRenderer, ]
