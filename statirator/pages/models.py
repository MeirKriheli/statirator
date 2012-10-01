from django.db import models
from django.conf import settings

from statirator.core.utils import i18n_permalink
from statirator.core.models import TranslationsMixin

PAGE_TYPES = (
    ('rst', 'reStructured Text'),
    ('html', 'Django template'),
)


class Page(models.Model, TranslationsMixin):
    """A multilingual page"""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    content = models.TextField()
    language = models.CharField(max_length=5, choices=settings.LANGUAGES,
                                blank=True, default=settings.LANGUAGE_CODE)
    page_type = models.CharField(max_length=5, choices=PAGE_TYPES)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.title or self.slug

    @i18n_permalink
    def get_absolute_url(self):
        # index is a special case
        if self.slug == 'index':
            return ('pages_index', (), {})

        return ('pages_page', (), {'slug': self.slug})
