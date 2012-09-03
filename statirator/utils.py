import logging


def find_walkers():
    """Auto discover walkers in installed apps.

    Each walkers.py should have the WALKERS list with walker classes
    """

    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    walkers = []
    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's admin module.
        try:
            walk_mod = import_module('%s.walkers' % app)
            if hasattr(walk_mod, 'WALKERS'):
                walkers.extend(walk_mod.WALKERS)
            else:
                logging.warn(
                    'walkers found in app %s, but has no WALKERS attrib',
                    app)
        except:
            # Decide whether to bubble up this error. If the app just
            # doesn't have an walkers module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'walkers'):
                raise

    return walkers
