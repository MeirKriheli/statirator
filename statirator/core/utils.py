import os
import logging


def find_readers():
    """Auto discover readers in installed apps.

    Each readers.py should have the READERS list with reader classes
    """

    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    readers = []
    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's admin module.
        try:
            walk_mod = import_module('%s.readers' % app)
            if hasattr(walk_mod, 'READERS'):
                readers.extend(walk_mod.READERS)
            else:
                logging.warn(
                    'readers found in app %s, but has no READERS attrib',
                    app)
        except:
            # Decide whether to bubble up this error. If the app just
            # doesn't have an readers module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'readers'):
                raise

    return readers


def find_files(root, extensions):
    """Generator finding files from a root dir with specific extensions

    :param root: Root directory for the search
    :param extensions: List of extensions to search (e.g: ['.rst', '.txt'])
    """

    for root, dirs, files in os.walk(root):
        for f in files:
            if os.path.splitext(f)[1] in extensions:
                yield os.path.join(root, f)
