from django.db import models
from django.conf import settings

from statirator.core.utils import i18n_permalink


class Page(models.Model):
    """A multilingual page"""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    content = models.TextField()
    language = models.CharField(max_length=5, choices=settings.LANGUAGES,
                                blank=True, default=settings.LANGUAGE_CODE)

    def __unicode__(self):
        return self.title

    @i18n_permalink
    def get_absolute_url(self):
        if self.slug == 'index':
            return ('pages_index', (), {})
