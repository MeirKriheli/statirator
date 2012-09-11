:slug: {{ slug }}
:draft: {{ draft  }}
:datetime: {% now "Y-m-d H:i:s" %}

{% comment %}
.. --
=================
English title
=================

:lang: en
:tags: Tag1, Tag2

The content of the English post

And another paragraph

.. --

====================
כותרת עברית
====================

:lang: he
:tags: פייתון|python, Heb Tag2|slug

The content of the post in Hebrew
""".decode('utf-8')
{% endcomment %}
