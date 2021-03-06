# Generated by statirator
import os

# directories setup

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
SOURCE_DIR = os.path.join(ROOT_DIR, '')
BUILD_DIR = os.path.join(ROOT_DIR, 'build')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SITE_ID = 1

# Local time zone. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Default Language code. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'he'
_ = lambda s: s

LANGUAGES = (
    ('en', _('English')),
    ('he', _('Hebrew')),
)

#ROOT_URLCONF = 'conf.urls'

TEMPLATE_DIRS = (
    os.path.join(ROOT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django_medusa',
    'taggit',
    'statirator.core',
    'statirator.blog',
)

MEDUSA_RENDERER_CLASS = "django_medusa.renderers.DiskStaticSiteRenderer"
MEDUSA_MULTITHREAD = True
MEDUSA_DEPLOY_DIR = BUILD_DIR
