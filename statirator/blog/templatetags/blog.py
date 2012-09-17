from __future__ import absolute_import
from django.conf import settings
from django.db.models import Count
from django.template.base import Node, Library, TemplateSyntaxError

from statirator.blog.models import I18NTag

register = Library()

# tag cloud from django-taggit-templatetags:
# https://github.com/feuervogel/django-taggit-templatetags

T_MAX = getattr(settings, 'TAGCLOUD_MAX', 6.0)
T_MIN = getattr(settings, 'TAGCLOUD_MIN', 1.0)


def get_queryset(language):
    qs = I18NTag.objects.filter(language=language)
    qs = qs.annotate(num_times=Count('blog_i18ntaggeditem_items'))
    return qs


def get_weight_fun(t_min, t_max, f_min, f_max):
    def weight_fun(f_i, t_min=t_min, t_max=t_max, f_min=f_min, f_max=f_max):
        # Prevent a division by zero here, found to occur under some
        # pathological but nevertheless actually occurring circumstances.
        if f_max == f_min:
            mult_fac = 1.0
        else:
            mult_fac = float(t_max - t_min) / float(f_max - f_min)

        return t_max - (f_max - f_i) * mult_fac
    return weight_fun


class TagListNode(Node):
    "Simple tag list, ordered by count"

    def __init__(self, language, asvar):
        self.language = language
        self.asvar = asvar

    def render(self, context):
        language = self.language.resolve(context)
        tags_qs = get_queryset(language).order_by('-num_times')

        if self.asvar:
            context[self.asvar] = tags_qs
            return ''
        else:
            return tags_qs


class TagCloudNode(Node):
    "Tag cloud list, ordered by name, has weight attribute"

    def __init__(self, language, asvar):
        self.language = language
        self.asvar = asvar

    def render(self, context):
        language = self.language.resolve(context)
        tags_qs = get_queryset(language).order_by('-num_times')

        num_times = tags_qs.values_list('num_times', flat=True)

        if num_times:
            weight_fun = get_weight_fun(T_MIN, T_MAX, min(num_times),
                                        max(num_times))
            tags_qs = tags_qs.order_by('name')
            for tag in tags_qs:
                tag.weight = weight_fun(tag.num_times)

        context[self.asvar] = tags_qs
        return ''


@register.tag
def get_taglist(parser, token):
    """Returns a tag list, sorted bt the number of tagged items.

    The first argument is the language code. specify "as" var e.g::

        {% get_taglist LANGUAGE_CODE as tags_list %}

    """
    bits = token.split_contents()

    if len(bits) != 4 and bits[2] != 'as':
        raise TemplateSyntaxError("Usage: '%s' language_code as"
                                  " context_var" % bits[0])

    language = parser.compile_filter(bits[1])
    asvar = bits[-1]

    return TagListNode(language, asvar)


@register.tag
def get_tagcloud(parser, token):
    """Returns a tag cloud, sorted by name and has the "weight" attribute.

    The first argument is the language code. specify "as" var e.g::

        {% get_taglist LANGUAGE_CODE as tags_list %}

    """
    bits = token.split_contents()

    if len(bits) != 4 and bits[2] != 'as':
        raise TemplateSyntaxError("Usage: '%s' language_code as"
                                  " context_var" % bits[0])

    language = parser.compile_filter(bits[1])
    asvar = bits[-1]

    return TagCloudNode(language, asvar)
