from django.conf import settings


def st_settings(request):
    """Return stuff """

    return {
        'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', None),
    }
