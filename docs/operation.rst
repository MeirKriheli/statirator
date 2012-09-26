==================
Modus operandi
==================

Init
============

The init command creates the basic project using a `custom project template`_.
``settings.py`` and ``urls.py`` are under ``conf`` dir.

.. _custom project template: https://docs.djangoproject.com/en/dev/releases/1.4/#custom-project-and-app-templates


Generating the site
======================

The following steps are done when generating the site

* Sync in memory db
* Create the site enrty for the `Sites` app.
* Read the resources (posts, pages) into the db using Readers_.
* Generate the static pages for those (and other) resources with Renderes_.
* Copy the static media to the build directory.

.. _Sites: https://docs.djangoproject.com/en/dev/ref/contrib/sites/


Readers
=============



Renderes
=============


Static media
=============
