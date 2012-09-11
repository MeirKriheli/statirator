import re
from docutils.core import publish_doctree
from docutils.nodes import docinfo
from datetime import datetime


FIELDS = {
    'slug': None,
    'title': None,
    'lang': None,
    'draft': lambda x: bool(int(x)),
    'tags': lambda x: [y.strip() for y in x.split(',')],
    'datetime': lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'),
}


def parse_rst(content):
    """Parse multilingual rst document. Content should contain a metadata
    section which is the same for all languages, and sections for each
    language. the sections should be separated by comment of "--"". e.g::

        :slug: some-post-title-slugified
        :draft: 1/0 (Defaulty in x.split(',')],
        :datetime: yyyy-mm-dd hh:mm:ss

        .. --

        :title: Some post title
        :lang: en
        :tags: Tag1, Tag2

        The content of the post

        .. --

        :title: The title in Hebrew
        :lang: he
        :tags: Heb Tag1|slug, Heb Tag2|slug

        The content of the post in hebrew

    Returned value is a genearator:

    common metadata, (metadata, content), (metadata, content) ...
    """

    parts = re.split(r'^\.\.\s+--\s*$', content, flags=re.M)
    for part in parts:
        content = ''
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

        yield metadata, content
