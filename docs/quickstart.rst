===============
Quick Start
===============

Installation
================

TODO


Initialize The Site
===================

Once installed, use the ``statirator init`` command to initialize the site. The
command reference::

    Usage: statirator init [options] [directory]

    Init the static site project

    Options:
    -t TITLE, --title=TITLE
                            Site title [Default: "Default site"]
    -d DOMAIN, --domain=DOMAIN
                            Domain name [Default: "example.com"]
    -l LANGUAGES, --languages=LANGUAGES
                            Supported languages. [Default: "['he', 'en']"]
    -z TIMEZONE, --timezone=TIMEZONE
                            Time Zone. [Default: "America/Chicago"]

Let's init the site::

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


Generate the Static Site
===========================

To generate the static site run the ``generate`` command. The will create the
static site in the ``BUILD_DIR`` directory (default: ``build``). Example run:

.. code-block:: sh


    [example.com]$ ./manage.py generate

    Syncing in memory db
    --------------------
    Creating tables ...
    Creating table django_content_type
    Creating table django_site
    Creating table taggit_tag
    Creating table taggit_taggeditem
    Creating table blog_i18ntag
    Creating table blog_i18ntaggeditem
    Creating table blog_post
    Creating table pages_page
    Installing custom SQL ...
    Installing indexes ...

    Reading resource
    ----------------
    Processing /home/meir/devel/Projects/meirkriheli/example.com/blog/welcome-to-my-blog.rst
    Processing /home/meir/devel/Projects/meirkriheli/example.com/pages/index.html

    Generating static pages
    -----------------------
    Skipping app 'conf'... (No 'renderers.py')
    Skipping app 'django.contrib.contenttypes'... (No 'renderers.py')
    Skipping app 'django.contrib.sites'... (No 'renderers.py')
    Skipping app 'django.contrib.staticfiles'... (No 'renderers.py')
    Skipping app 'taggit'... (No 'renderers.py')
    Skipping app 'disqus'... (No 'renderers.py')
    Skipping app 'statirator.core'... (No 'renderers.py')
    Found renderers for 'statirator.blog'...
    Found renderers for 'statirator.pages'...

    example.com/build/en/2012/09/welcome-to-my-blog/index.html
    example.com/build/en/archive/index.html
    example.com/build/en/blog.rss
    example.com/build/2012/09/welcome-to-my-blog/index.html
    example.com/build/archive/index.html
    example.com/build/blog.rss
    example.com/build/en/tags/tag-1/index.html
    example.com/build/en/tags/tag-2/index.html
    example.com/build/en/tags/tag-1/tag.rss
    example.com/build/en/tags/tag-2/tag.rss
    example.com/build/en/tags/index.html
    example.com/build/tags/tag-1/index.html
    example.com/build/tags/tag-2/index.html
    example.com/build/tags/tag-1/tag.rss
    example.com/build/tags/tag-2/tag.rss
    example.com/build/tags/index.html
    example.com/build/en/index.html
    example.com/build/index.html

    Collecting static media
    -----------------------
    example.com/static/crossdomain.xml'
    example.com/static/humans.txt'
    example.com/static/robots.txt'
    example.com/static/favicon.ico'
    example.com/static/img/apple-touch-icon-precomposed.png'
    example.com/static/img/apple-touch-icon-114x114-precomposed.png'
    example.com/static/img/apple-touch-icon-57x57-precomposed.png'
    example.com/static/img/apple-touch-icon.png'
    example.com/static/img/apple-touch-icon-144x144-precomposed.png'
    example.com/static/img/apple-touch-icon-72x72-precomposed.png'
    example.com/static/js/main.js'
    example.com/static/js/plugins.js'
    example.com/static/js/vendor/jquery-1.8.0.min.js'
    example.com/static/js/vendor/modernizr-2.6.1.min.js'
    example.com/static/css/normalize.css'
    example.com/static/css/main.css'
    example.com/static/css/normalize_rtl.css'

    17 static files copied.
