.. Statirator documentation master file, created by
   sphinx-quickstart on Sun Sep 23 01:34:44 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Statirator's documentation!
======================================

Multilingual static site and blog generator.

Reason
--------

* Needed good multilingual static site generator, which enables:

  * Explicitly specifying slug for various non-Latin links in addition to posts
    (e.g: Tag names, pages, etc.)
  * Separate RSS feeds for each language and each tag/language
  * Keeps reference between the translations
  * Optional Multi-domain support - One for each language (TODO)
  * Translated elements in pages

* No need to reinvent the wheel:

  * Many know Django_, we can reuse the knowledge
  * Make use of reusable apps
  * Hack around i18n bits of Django_.
  * Use Django_'s `Internationalization and localization`_

Contents:

.. _Django: https://www.djangoproject.com/
.. _Internationalization and localization: https://docs.djangoproject.com/en/1.4/topics/i18n/

.. toctree::
    :maxdepth: 2

    quickstart



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

