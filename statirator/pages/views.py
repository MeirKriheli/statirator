from __future__ import absolute_import

from django.views.generic.detail import DetailView
from django.template import Template
from django.template.response import TemplateResponse
from .models import Page


class PageView(DetailView):

    model = Page

    def get_queryset(self):

        qs = Page.objects.filter(language=self.request.LANGUAGE_CODE)
        return qs

    def render_to_response(self, context, **response_kwargs):
        # if this is html content, it's a template, and we should render it
        if self.object.page_type == 'html':
            t = Template(self.object.content)
            return TemplateResponse(self.request, t)

        return super(self, PageView).render_to_response(
            context, **response_kwargs)
