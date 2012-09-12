from __future__ import absolute_import

from django.conf import settings
from django.utils.translation import activate
from django_medusa.renderers import StaticSiteRenderer

from .models import Post


class BlogRenderer(StaticSiteRenderer):

    def get_paths(self):

        paths = []
        for lang_code, lang_name in settings.LANGUAGES:
            activate(lang_code)
            items = Post.objects.filter(
                is_published=True, language=lang_code).order_by('-pubdate')

            paths.extend([i.get_absolute_url() for i in items])

        return paths

renderers = [BlogRenderer, ]
