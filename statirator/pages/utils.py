from __future__ import absolute_import
import os


def get_pages_dir():
    "Returns the pages directory from settings, or default one if not found"

    from django.conf import settings

    return getattr(settings, 'PAGES_DIR',
                   os.path.join(settings.ROOT_DIR, 'pages'))
