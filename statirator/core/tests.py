# -*- coding: utf-8 -*-
import datetime
from django.utils import unittest
from statirator.core.utils import find_readers
from statirator.core.readers import dummy_reader
from statirator.core.parsers import parse_rst


TEST_DOC = """
:slug: some-post-title-slugified
:draft: 1
:datetime: 2012-09-12 16:03:15

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
""".decode('utf-8')


class CoreTestCase(unittest.TestCase):

    def test_find_readers(self):
        "Correctly find readers"

        readers = find_readers()
        self.assertIn(dummy_reader, readers)

    def test_rst_parser(self):
        """Correctly parse multilingual rst documents"""

        parsed = parse_rst(TEST_DOC)
        generic_metadata, title, content = parsed.next()
        self.assertEqual(generic_metadata, {
            'slug': 'some-post-title-slugified',
            'draft': True,
            'datetime': datetime.datetime(2012, 9, 12, 16, 3, 15),
        })
        self.assertEqual(content.strip(),
                         u'<p>This will be ignored in main meta section</p>')

        en_metadata, en_title, en_content = parsed.next()
        self.assertEqual(en_metadata, {'lang': 'en', 'tags': ['Tag1', 'Tag2']})
        self.assertEqual(en_title, u'English title')
        self.assertEqual(en_content.strip(),
                         u'<p>The content of the English post</p>\n'
                         u'<p>And another paragraph</p>')

        he_metadata, he_title, he_content = parsed.next()
        self.assertEqual(he_metadata, {
            'lang': 'he',
            'tags': ['פייתון|python'.decode('utf-8'), 'Heb Tag2|slug']
        })
        self.assertEqual(he_title, 'כותרת עברית'.decode('utf-8'))
        self.assertEqual(he_content.strip(),
                         u'<p>The content of the post in Hebrew</p>')
