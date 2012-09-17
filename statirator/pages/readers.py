from __future__ import print_function, absolute_import

from statirator.core.utils import find_files
from statirator.core.parsers import parse_rst
from .utils import get_pages_dir
from .models import Page


def rst_reader():
    "Finds rst posts, parses them and loads into the db."

    for page in find_files(get_pages_dir(), ['.rst']):
        print('Processing {0}'.format(page))
        with open(page) as p:
            parsed = parse_rst(p.read())

            generic_metadata, title, content = parsed.next()

            # got those, now go over the languages
            for metadata, title, content in parsed:
                lang = metadata['lang']

                page = Page(
                    title=title,
                    slug=generic_metadata['slug'],
                    content=content,
                    language=lang)
                page.save()

READERS = [rst_reader]
