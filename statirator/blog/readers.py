from __future__ import print_function
import os

from statirator.core.utils import find_files
from statirator.core.parsers import parse_rst


def get_blog_dir():
    "Returns the blog directory from settings, or default one if not found"

    from django.conf import settings

    return getattr(settings, 'BLOG_DIR', os.path.join(settings.ROOT_DIR, 'blog'))


def rst_reader():
    "Finds rst posts, parses them and loads into the db."

    for post in find_files(get_blog_dir(), ['.rst']):
        print('Processing {0}'.format(post))
        with open(post) as p:
            parsed = parse_rst(p.read())


READERS = [rst_reader]
