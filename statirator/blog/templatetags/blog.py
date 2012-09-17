from __future__ import absolute_import
from django.db.models import Count
from django.template.base import Node, Library, TemplateSyntaxError

from statirator.blog.models import I18NTag

register = Library()


def get_queryset(language):
    qs = I18NTag.objects.filter(language=language)
    qs = qs.annotate(num_times=Count('blog_i18ntaggeditem_items'))
    return qs


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


@register.tag
def get_taglist(parser, token):
    """Returns a tag list, sorted bt the number of tagged items.

    The first argument is the language code. e.g::

        {% get_taglist LANGUAGE_CODE %}

    Optionaly specify "as" to get it into a context var, e.g::

        {% get_taglist LANGUAGE_CODE as tags_list %}

    """
    bits = token.split_contents()

    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (language)" % bits[0])

    language = parser.compile_filter(bits[1])
    asvar = None

    if len(bits) >= 3 and bits[-2] == 'as':
        asvar = bits[-1]

    return TagListNode(language, asvar)
