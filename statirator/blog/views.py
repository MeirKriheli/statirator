from __future__ import absolute_import

from django.views.generic.detail import DetailView
from .models import Post


class PostView(DetailView):

    def get_queryset(self):
        qs = Post.objects.filter(language=self.request.LANGUAGE_CODE)

        return qs
