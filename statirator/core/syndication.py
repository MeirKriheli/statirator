from django.conf import settings
from django.contrib.syndication.views import Feed


class LanguageFeed(Feed):
    """Stores the request language in `language_code` attribute, and sets
    the feed's language to the apropriate one.
    """

    def get_feed(self, obj, request):
        "Override to get items per language"

        try:
            self.language_code = request.LANGUAGE_CODE  # store it for later
        except AttributeError:
            self.language_code = settings.LANGUAGE_CODE

        feed = super(LanguageFeed, self).get_feed(obj, request)
        feed.feed['language'] = self.language_code

        return feed
