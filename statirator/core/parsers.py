import re
from docutils.core import publish_doctree


def parse_rst(content):
    """Parse multilingual rst document. Content should contain a metadata
    section which is the same for all languages, and sections for each
    language. the sections should be separated by comment of "--"". e.g::

        :slug: some-post-title-slugified
        :draft: 1/0 (Default assumes that it's published)
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

        tree = publish_doctree(part).asdom()

        # get the fields
        fields = tree.getElementsByTagName('field')

        for field in fields:
            nodes = zip(field.getElementsByTagName('field_name'),
                        field.getElementsByTagName('field_body'))
            metadata.update(dict((n[0].firstChild.nodeValue, n[1].firstChild.firstChild.nodeValue) for n in nodes))

        yield metadata, content
