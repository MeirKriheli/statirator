from __future__ import absolute_import
import os


def get_blog_dir():
    "Returns the blog directory from settings, or default one if not found"

    from django.conf import settings

    return getattr(settings, 'BLOG_DIR', os.path.join(settings.ROOT_DIR, 'blog'))
