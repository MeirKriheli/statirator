from django.conf import settings
from django.contrib.sites.models import Site


def st_settings(request):
    """Return stuff """

    return {
        'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', None),
        'POSTS_IN_INDEX': getattr(settings, 'POSTS_IN_INDEX', 5),
        'site': Site.objects.get_current()
    }
