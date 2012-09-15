import os
import logging
import functools


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


def i18n_permalink(*args):
    """Return the correct URL in case of not the default language.
    relaces djangos models.permalink.

    Assumes the name of the i18n version of the url pattern is prefix with
    'i18n_' (This is done in the statirator's default urls.py).

    It looks for a `language` field for the instance. If the name is different,
    pass it as the first param to the decorator. e.g::

        @i18n_permalink('lang_code')
        def get_absolute_url(self):
            return (...)

    """
    def outer(f):
        @functools.wraps(f)
        def wrapper(obj, *args, **kwargs):

            bits = f(obj, *args, **kwargs)
            name = bits[0]

            lang = getattr(obj, language_field)
            return i18n_reverse(lang, name, None, *bits[1:3])

        return wrapper

    if len(args) == 1 and callable(args[0]):
        # No arguments, this is the decorator
        # Set default values for the arguments
        language_field = 'language'
        return outer(args[0])
    else:
        language_field = args[0]
        return outer


def i18n_reverse(language, viewname, *args, **kwargs):
    """Django's reverse with a pinch of i18n.

    Assumes the name of the i18n version of the url pattern is prefix with
    'i18n_' (This is done in the statirator's default urls.py).

    """
    from django.core.urlresolvers import reverse
    from django.conf import settings
    from django.utils.translation import activate, get_language

    cur_lang = get_language()

    # activate the obj's lang for correct i18n_patterns reverse
    activate(language)
    if language != settings.LANGUAGE_CODE:
        viewname = 'i18n_' + viewname

    res = reverse(viewname, *args, **kwargs)
    activate(cur_lang)

    return res
