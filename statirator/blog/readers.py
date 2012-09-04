from __future__ import print_function
import os
import logging

from statirator.utils import find_files


def get_blog_dir():
    "Returns the blog directory from settings, or default one if not found"

    from django.conf import settings

    return getattr(settings, 'BLOG_DIR', os.path.join(settings.ROOT_DIR, 'blog'))


def rst_reader():
    """Reader rst posts"""

    for post in find_files(get_blog_dir(), ['.rst']):
        print('Processing {0}'.format(post))


READERS = [rst_reader]
