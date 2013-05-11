from __future__ import absolute_import
import os


def get_blog_dir():
    "Returns the blog directory from settings, or default one if not found"

    from django.conf import settings

    return getattr(settings, 'BLOG_DIR',
                   os.path.join(settings.ROOT_DIR, 'blog'))


_post_keys = None


def get_post_urlpattern_keys():
    """Returns the keys defined for the blog's url pattern, to correctly
    calculate the post's permalink"""

    global _post_keys

    if _post_keys is None:
        from django.core import urlresolvers

        conf = urlresolvers.get_urlconf()
        resolver = urlresolvers.get_resolver(conf)

        try:
            # get the 1st pattern matching 'blog_post'
            post_re_pattern = (
                x for x in resolver.url_patterns
                if getattr(x, 'name', None) == 'blog_post'
            ).next()
        except StopIteration:
            raise Exception('URL pattern named "blog_post" not found')

        _post_keys = post_re_pattern.regex.groupindex.keys()

    return _post_keys
