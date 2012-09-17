from __future__ import absolute_import

from django.views.generic.detail import DetailView
from .models import Page


class PageView(DetailView):

    model = Page

    def get_queryset(self):

        qs = Page.objects.filter(language=self.request.LANGUAGE_CODE)
        return qs
