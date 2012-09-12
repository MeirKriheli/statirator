from __future__ import print_function, absolute_import

from statirator.core.utils import find_files
from statirator.core.parsers import parse_rst
from .utils import get_blog_dir
from .models import I18NTag, Post


def rst_reader():
    "Finds rst posts, parses them and loads into the db."

    for post in find_files(get_blog_dir(), ['.rst']):
        print('Processing {0}'.format(post))
        with open(post) as p:
            parsed = parse_rst(p.read())

            generic_metadata, title, content = parsed.next()

            # got those, now go over the languages
            for metadata, title, content in parsed:
                post = Post(
                    title=title,
                    slug=generic_metadata['slug'],
                    is_published=generic_metadata['draft'],
                    content=content,
                    pubdate=generic_metadata['datetime'],
                    language=metadata['lang'])
            post.save()
            # TODO handle tags

READERS = [rst_reader]
