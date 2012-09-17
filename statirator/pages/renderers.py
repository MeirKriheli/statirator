from __future__ import absolute_import

from django.conf import settings
from django.utils.translation import activate
from django_medusa.renderers import StaticSiteRenderer

from .models import Page


class PagesRenderer(StaticSiteRenderer):

    def get_paths(self):

        paths = []

        for lang_code, lang_name in settings.LANGUAGES:
            activate(lang_code)
            items = Page.objects.filter(language=lang_code)
            paths.extend([i.get_absolute_url() for i in items])

        return paths


renderers = [PagesRenderer]
