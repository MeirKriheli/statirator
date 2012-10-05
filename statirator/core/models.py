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
