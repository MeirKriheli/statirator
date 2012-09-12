{% load i18n %}{% get_current_language as LANGUAGE_CODE %}{% get_language_info for LANGUAGE_CODE as lang %}
{% trans "Tag" as tag_i18n  %}{% trans "Title" as title_i18n %}
=============================================================
{% if LANGUAGE_CODE == 'en' %}{{title|safe}}{% else %}{% blocktrans with lang.name_local as lang_name %}{{lang_name}} {{ title_i18n }}{% endblocktrans %}{% endif %}
=============================================================

:lang: {{ LANGUAGE_CODE }}
:tags:  {{ tag_i18n }} 1|tag-1, {{ tag_i18n }} 2|tag-2

{% blocktrans with lang.name_local as lang_name %}{{ lang_name }} content goes here{% endblocktrans %}
