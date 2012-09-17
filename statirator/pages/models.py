from django.db import models
from django.conf import settings


class Page(models.Model):
    """A multilingual page"""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    content = models.TextField()
    language = models.CharField(max_length=5, choices=settings.LANGUAGES,
                                blank=True, default=settings.LANGUAGE_CODE)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('view_or_url_name')
