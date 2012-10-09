from __future__ import absolute_import
from django.conf import settings
from .utils import path_to_lang, LANGS_DICT


class TranslationsMixin(object):
    "Helper for getting transalations"

    SLUG_FIELD_FOR_TRANSLATIONS = 'slug'      # Overide in models if needed
    LANG_FIELD_FOR_TRANSLATIONS = 'language'  # Overide in models if needed

    def get_translations(self):
        "Query set for the translations"

        self_slug = getattr(self, self.SLUG_FIELD_FOR_TRANSLATIONS)
        self_lang = getattr(self, self.LANG_FIELD_FOR_TRANSLATIONS)

        slug = {self.SLUG_FIELD_FOR_TRANSLATIONS + '__exact': self_slug}
        lang = {self.LANG_FIELD_FOR_TRANSLATIONS + '__exact': self_lang}
        return self.__class__.objects.filter(**slug).exclude(**lang)

    def get_language(self):
        "Get the language display for this item's language"

        attr = 'get_{0}_display'.format(self.LANG_FIELD_FOR_TRANSLATIONS)
        return getattr(self, attr)()


class DummyTranslation(object):
    """Dummy translations for views to put in template context in case there's no
    actual object"""

    def __init__(self, request, language=None, title=None, path=None):
        self.title = title
        self.request = request
        self.language = language or request.LANGUAGE_CODE
        self.path = path or request.path

    def get_translations(self):
        for code, name in settings.LANGUAGES:
            if code != self.language:
                yield DummyTranslation(self.request, code, name, self.path)

    def get_language(self):
        return LANGS_DICT.get(self.language)

    def get_absolute_url(self):
        return path_to_lang(self.path, self.language)
