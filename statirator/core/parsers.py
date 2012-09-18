# -*- coding: utf-8 -*-
import re
from datetime import datetime
from docutils.core import publish_doctree, publish_from_doctree, publish_parts
from docutils.nodes import docinfo
from html5writer import html5writer


def _publish_body(source):
    """Returns the published body of rst source"""
    content = publish_parts(source, writer=html5writer.SemanticHTML5Writer())
    return content['body']


FIELDS = {
    'slug': None,
    'title': None,
    'lang': None,
    'draft': lambda x: bool(int(x)),
    'tags': lambda x: [y.strip() for y in x.split(',')],
    'datetime': lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'),
    'excerpt': _publish_body,
    'image': None,
}


def parse_rst(content):
    """Parse multilingual rst document. Content should contain a metadata
    section which is the same for all languages, and sections for each
    language. the sections should be separated by comment of "--"". e.g::

        :slug: some-post-title-slugified
        :draft: 1
        :datetime: 2012-09-12 16:03:15
        :excerpt: Short description
        :image: /img/some_image.png

        This will be ignored in main meta section

        .. --

        =================
        English title
        =================

        :lang: en
        :tags: Tag1, Tag2

        The content of the English post

        And another paragraph

        .. --

        ====================
        כותרת עברית
        ====================

        :lang: he
        :tags: פייתון|python, Heb Tag2|slug

        The content of the post in Hebrew

    Returned value is a genearator:

    (common metadata, '', content), (metadata, title, content), (metadata, title, content) ...
    """

    parts = re.split(r'^\.\.\s+--\s*$', content, flags=re.M)

    for part in parts:
        content = ''
        title = ''
        metadata = {}

        tree = publish_doctree(part)

        for info in tree.traverse(docinfo):
            for field in info.children:
                    name_el, body_el = field.children
                    name = name_el.astext().lower()
                    if name in FIELDS:
                        body = body_el.astext()
                        transform = FIELDS[name]

                        metadata[name] = transform(body) if transform else body

        writer = html5writer.SemanticHTML5Writer()
        publish_from_doctree(tree, writer=writer)
        content = writer.parts['body']
        title = writer.parts['title']
        yield metadata, title, content
