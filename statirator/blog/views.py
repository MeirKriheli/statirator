from __future__ import absolute_import

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Post, I18NTag


class PostView(DetailView):

    models = Post

    def get_queryset(self):
        qs = Post.objects.filter(language=self.request.LANGUAGE_CODE)
        return qs


class ArchiveView(ListView):

    models = Post

    def get_queryset(self):
        qs = Post.objects.filter(language=self.request.LANGUAGE_CODE,
                                 is_published=True).order_by('-pubdate')
        return qs


class TagView(DetailView):

    model = I18NTag

    def get_object(self):

        return I18NTag.objects.get(language=self.request.LANGUAGE_CODE,
                                   slug_no_locale=self.kwargs['slug'])

    def get_context_data(self, **kwargs):

        ctx = super(TagView, self).get_context_data(**kwargs)

        tag = ctx['object']

        ctx['posts'] = Post.objects.filter(
            language=self.request.LANGUAGE_CODE,
            is_published=True,
            tags__slug__in=[tag.slug]).order_by('-pubdate')

        return ctx


class TagsView(ListView):

    model = I18NTag

    def get_queryset(self):
        qs = I18NTag.objects.filter(language=self.request.LANGUAGE_CODE)
        return qs
