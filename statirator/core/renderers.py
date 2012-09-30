from __future__ import absolute_import

from django.core.urlresolvers import reverse
from django_medusa.renderers import StaticSiteRenderer


class CoreRenderer(StaticSiteRenderer):

    def get_paths(self):

        paths = [reverse('sitemap')]

        return paths


renderers = [CoreRenderer]
