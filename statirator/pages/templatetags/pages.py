from __future__ import absolute_import

from django.template.base import Node, Library, TemplateSyntaxError
from statirator.pages.models import Page

register = Library()


class PagesNode(Node):
    """Pages list"""

    def __init__(self, language, asvar):
        self.language = language
        self.asvar = asvar

    def render(self, context):
        language = self.language.resolve(context)

        pages = Page.objects.filter(language=language)

        context[self.asvar] = pages
        return ''


@register.tag
def get_pages(parser, token):
    """Returns a tag cloud, sorted by name and has the "weight" attribute.

    The first argument is the language code. specify "as" var e.g::

        {% get_pages LANGUAGE_CODE as pages_list %}

    """
    bits = token.split_contents()

    if len(bits) != 4 and bits[2] != 'as':
        raise TemplateSyntaxError("Usage: '%s' language_code as"
                                  " context_var" % bits[0])

    language = parser.compile_filter(bits[1])
    asvar = bits[-1]

    return PagesNode(language, asvar)
