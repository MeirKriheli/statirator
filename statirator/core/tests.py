from django.utils import unittest
from statirator.core.utils import find_readers
from statirator.core.readers import dummy_reader


class CoreTestCase(unittest.TestCase):

    def test_find_readers(self):
        "Correctly find readers"

        readers = find_readers()
        self.assertIn(dummy_reader, readers)
