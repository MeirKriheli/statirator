from __future__ import print_function, absolute_import

from statirator.core.utils import find_files
from statirator.core.parsers import parse_rst
from .utils import get_blog_dir


def rst_reader():
    "Finds rst posts, parses them and loads into the db."

    for post in find_files(get_blog_dir(), ['.rst']):
        print('Processing {0}'.format(post))
        with open(post) as p:
            parsed = parse_rst(p.read())

            metadata = parsed.next()
            print(metadata)

READERS = [rst_reader]
