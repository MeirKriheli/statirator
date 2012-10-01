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


class PageNode(Node):
    "Get a single page"

    def __init__(self, language, slug, asvar):
        self.language = language
        self.slug = slug
        self.asvar = asvar

    def render(self, context):
        language = self.language.resolve(context)
        slug = self.slug.resolve(context)

        page = Page.objects.get(language=language, slug=slug)

        context[self.asvar] = page
        return ''


@register.tag
def get_pages(parser, token):
    """Returns all pages.

    The first argument is the language code. specify "as" var e.g::

        {% get_pages LANGUAGE_CODE as pages_list %}

    """
    bits = token.split_contents()

    if len(bits) != 4 and bits[2] != 'as':
        raise TemplateSyntaxError("Usage: %s language_code as"
                                  " context_var" % bits[0])

    language = parser.compile_filter(bits[1])
    asvar = bits[-1]

    return PagesNode(language, asvar)


@register.tag
def get_page(parser, token):
    """Returns a page base on slug and language.

    The first argument is the language code, 2nd is slug. specify "as" var e.g::

        {% get_page LANGUAGE_CODE "index" as index_page %}

    """
    bits = token.split_contents()

    if len(bits) != 5 and bits[3] != 'as':
        raise TemplateSyntaxError('Usage: %s language_code "slug" as'
                                  " context_var" % bits[0])

    language = parser.compile_filter(bits[1])
    slug = parser.compile_filter(bits[2])
    asvar = bits[-1]

    return PageNode(language, slug, asvar)
