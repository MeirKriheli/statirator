import datetime
from django.utils import unittest
from statirator.core.utils import find_readers
from statirator.core.readers import dummy_reader
from statirator.core.parsers import parse_rst


TEST_DOC = """
:slug: some-post-title-slugified
:draft: 1
:datetime: 2012-09-12 16:03:15

.. --

=================
Some post title
=================

:lang: en
:tags: Tag1, Tag2

The content of the post

.. --

====================
The title in Hebrew
====================

:lang: he
:tags: Heb Tag1|slug, Heb Tag2|slug

The content of the post in hebrew
"""


class CoreTestCase(unittest.TestCase):

    def test_find_readers(self):
        "Correctly find readers"

        readers = find_readers()
        self.assertIn(dummy_reader, readers)

    def test_rst_parser(self):
        """Correctly parse multilingual rst documents"""

        parsed = parse_rst(TEST_DOC)
        generic_metadata, content = parsed.next()
        self.assertEqual(generic_metadata, {
            'slug': 'some-post-title-slugified',
            'draft': True,
            'datetime': datetime.datetime(2012, 9, 12, 16, 3, 15),
        })
