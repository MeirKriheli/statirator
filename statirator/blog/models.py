from django.db import models, IntegrityError
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, TagBase, atomic

from statirator.core.utils import i18n_permalink
from statirator.core.models import TranslationsMixin


@python_2_unicode_compatible
class I18NTag(models.Model, TranslationsMixin):
    """Extend Taggit's Tag:

    * Add a language field
    * slug will be appended the locale, since we can't override the uniqute in
      the abstract model
    * slug_no_locale will have the actual slug

    """

    SLUG_FIELD_FOR_TRANSLATIONS = 'slug_no_locale'  # we need to override this

    name = models.CharField(verbose_name=_('Name'), max_length=100)
    slug = models.SlugField(verbose_name=_('Slug'), unique=True,
                            max_length=100)
    language = models.CharField(max_length=5, choices=settings.LANGUAGES,
                                blank=True, default=settings.LANGUAGE_CODE)
    slug_no_locale = models.SlugField(verbose_name=_('Slug without locale'),
                                      unique=False, max_length=100)

    class Meta:
        unique_together = ('language', 'slug_no_locale')

    @i18n_permalink
    def get_absolute_url(self):
        return ('blog_tag', (), {'slug': self.slug_no_locale})

    @i18n_permalink
    def get_feed_url(self):
        return ('blog_tag_feed', (), {'slug': self.slug_no_locale})

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = self.slugify(self.name)
            from django.db import router
            using = kwargs.get("using") or router.db_for_write(
                type(self), instance=self)
            # Make sure we write to the same db for all attempted writes,
            # with a multi-master setup, theoretically we could try to
            # write and rollback on different DBs
            kwargs["using"] = using
            # Be oportunistic and try to save the tag, this should work for
            # most cases ;)
            try:
                with atomic(using=using):
                    res = super(I18NTag, self).save(*args, **kwargs)
                return res
            except IntegrityError:
                pass
            # Now try to find existing slugs with similar names
            slugs = set(I18NTag.objects.filter(slug__startswith=self.slug)
                        .values_list('slug', flat=True))
            i = 1
            while True:
                slug = self.slugify(self.name, i)
                if slug not in slugs:
                    self.slug = slug
                    # We purposely ignore concurrecny issues here for now.
                    # (That is, till we found a nice solution...)
                    return super(I18NTag, self).save(*args, **kwargs)
                i += 1
        else:
            return super(I18NTag, self).save(*args, **kwargs)

    __str__ = TagBase.__str__
    slugify = TagBase.slugify


class I18NTaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(I18NTag,
                            related_name="%(app_label)s_%(class)s_items")


class Post(models.Model, TranslationsMixin):
    """Multilingual blog posts"""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    is_published = models.BooleanField(default=True, max_length=200)
    excerpt = models.TextField(blank=True, null=True)
    content = models.TextField()
    pubdate = models.DateTimeField(db_index=True)
    language = models.CharField(max_length=5, choices=settings.LANGUAGES,
                                blank=True, default=settings.LANGUAGE_CODE)
    image = models.CharField(max_length=255, blank=True, null=True)

    tags = TaggableManager(through=I18NTaggedItem)

    def __unicode__(self):
        return self.title

    @i18n_permalink
    def get_absolute_url(self):
        from .utils import get_post_urlpattern_keys

        keys = get_post_urlpattern_keys()

        kwargs = {k: getattr(self, k) for k in keys}

        return ('blog_post', (), kwargs)

    def get_next(self):
        return self.get_next_by_pubdate(language=self.language,
                                        is_published=True)

    def get_previous(self):
        return self.get_previous_by_pubdate(language=self.language,
                                            is_published=True)

    @property
    def tags_list(self):
        return self.tags.values_list('name', flat=True)

    @property
    def year(self):
        return self.pubdate.year

    @property
    def month(self):
        """Get a 2 digit formatted month"""
        return self.pubdate.strftime('%m')

    @property
    def day(self):
        """Get a 2 digit formatted day"""
        return self.pubdate.strftime('%d')
