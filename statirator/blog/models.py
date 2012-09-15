from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, TagBase

from statirator.core.utils import i18n_permalink


class I18NTag(TagBase):
    """Extend Taggit's Tag:

    * Add a language field
    * slug will be appended the locale, since we can't override the uniqute in
      the abstract model
    * slug_no_locale will have the actual slug

    """
    language = models.CharField(max_length=5, choices=settings.LANGUAGES,
                                blank=True, default=settings.LANGUAGE_CODE)
    slug_no_locale = models.SlugField(verbose_name=_('Slug without locale'),
                                      unique=False, max_length=100)

    class Meta:
        unique_together = ('language', 'slug_no_locale')

    @i18n_permalink
    def get_absolute_url(self):
        return ('blog_tag', (), {'slug': self.slug_no_locale})


class I18NTaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(I18NTag, related_name="%(app_label)s_%(class)s_items")


class Post(models.Model):
    """Multilingual blog posts"""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    is_published = models.BooleanField(default=True, max_length=200)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    pubdate = models.DateTimeField(db_index=True)
    language = models.CharField(max_length=5, choices=settings.LANGUAGES,
                                blank=True, default=settings.LANGUAGE_CODE)

    tags = TaggableManager(through=I18NTaggedItem)

    def __unicode__(self):
        return self.title

    @i18n_permalink
    def get_absolute_url(self):
        return ('blog_post', (), {
            'year': self.pubdate.year,
            'month': self.pubdate.strftime('%m'),
            'slug': self.slug,
        })
