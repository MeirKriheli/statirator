from __future__ import print_function
import os

from statirator.utils import find_files


def get_blog_dir():
    "Returns the blog directory from settings, or default one if not found"

    from django.conf import settings

    return getattr(settings, 'BLOG_DIR', os.path.join(settings.ROOT_DIR, 'blog'))


def rst_reader():
    """Reader rst posts, each post should be in the sections separated by
    comment of "sep"" with example sections in the format:

    Generic fields for all languages, e.g:

    :slug: some-post-title-slugified
    :draft: 1/0 (Default assumes that it's published)
    :date: yyyy-mm-dd hh:mm:ss

    .. sep

    :title: Some post title
    :lang: en
    :tags: Tag1, Tag2

    The content of the post

    .. sep

    :title: The title in Hebrew
    :lang: he
    :tags: Heb Tag1|slug, Heb Tag2|slug

    The content of the post in hebrew
    """

    for post in find_files(get_blog_dir(), ['.rst']):
        print('Processing {0}'.format(post))


READERS = [rst_reader]
