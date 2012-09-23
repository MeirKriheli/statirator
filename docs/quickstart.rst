===============
Quick Start
===============

Installation
================

TODO


Initialize The Site
===================

Once installed, use the ``statirator`` command to initialize the site::

    statirator init example.com

This will create ``example.com`` directory and the default site skeleton based
on `html5 boilerplate`_:

.. code-block:: sh

    $ tree example.com/
    example.com/
    |-- blog
    |   `-- README
    |-- conf
    |   |-- __init__.py
    |   |-- settings.py
    |   `-- urls.py
    |-- locale
    |   `-- README
    |-- manage.py
    |-- pages
    |   `-- index.html
    |-- static
    |   |-- crossdomain.xml
    |   |-- css
    |   |   |-- main.css
    |   |   |-- normalize.css
    |   |   `-- normalize_rtl.css
    |   |-- favicon.ico
    |   |-- humans.txt
    |   |-- img
    |   |   |-- apple-touch-icon-114x114-precomposed.png
    |   |   |-- apple-touch-icon-144x144-precomposed.png
    |   |   |-- apple-touch-icon-57x57-precomposed.png
    |   |   |-- apple-touch-icon-72x72-precomposed.png
    |   |   |-- apple-touch-icon.png
    |   |   `-- apple-touch-icon-precomposed.png
    |   |-- js
    |   |   |-- main.js
    |   |   |-- plugins.js
    |   |   `-- vendor
    |   |       |-- jquery-1.8.0.min.js
    |   |       `-- modernizr-2.6.1.min.js
    |   `-- robots.txt
    `-- templates
        `-- README

    10 directories, 25 files

.. _html5 boilerplate: http://html5boilerplate.com/


Notable directories and files:

* ``blog``: posts location
* ``conf``: The django project's settings and url patterns.
* ``manage.py``: Django's manage.py_. Will be used from now on.
* ``pages``: Site's pages (non blog posts, e,g: ``about us``).
* ``static``: Static media files. The files under that directory will be copied
  as is.
* ``templates``: Used override the default templates by placing them here.

.. _manage.py: https://docs.djangoproject.com/en/1.4/ref/django-admin/


Create a Blog Post
====================

Use the ``create_post`` management command. reference::

    Usage: ./manage.py create_post [options] <english title or slug>

    Create a new rst blog post

    Options:
    -d, --draft           Is is a draft (unpublished) ? [Default: "False"]

So for example::

    $ ./manage.py create_post "Welcome to my blog"

Will create a stub for that blog post:

.. code-block:: sh


    $ ls -1 blog/
    README
    welcome-to-my-blog.rst
    

Default Post Structure
===========================

Here's the content of the post:

.. code-block:: rst


    :slug: welcome-to-my-blog
    :draft: 0
    :datetime: 2012-09-22 19:16:45

    .. --

    =============================================================
    Welcome to my blog
    =============================================================

    :lang: en
    :tags:  Tag 1|tag-1, Tag 2|tag-2

    English content goes here

    .. --

    =============================================================
    כותרת עברית
    =============================================================

    :lang: he
    :tags:  תג 1|tag-1, תג 2|tag-2

    תוכן עברית יבוא כאן


This is valid reStructuredText document. The content sections are separated with
``.. --`` (which is interpreted as comment by reStructuredText). Metadata is
specified with fields_.

.. _fields: http://docutils.sourceforge.net/docs/user/rst/quickref.html#field-lists


The 1st section is generic metadata for the post.

Following sections are one per language (``lang`` is mandatory). As you can see,
the tags are comma separated and each specifies a tag name and it's slug,
separated by ``|``. After the metadata for each language comes the content.
