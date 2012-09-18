# Generated by statirator
import os

# Directories setup
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
SOURCE_DIR = os.path.join(ROOT_DIR, '{{ source }}')
BUILD_DIR = os.path.join(ROOT_DIR, '{{ build }}')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}


# Site(s) definitions. The Sites will be created when generate is called
# Each site is (domain, language, title). language of None means all
SITES = (
    ('{{ domain }}', None, '{{ title }}'),
)

SITE_ID = 1

# Local time zone. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = '{{ timezone  }}'

# Default Language code. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = '{{ default_lang }}'
_ = lambda s: s

LANGUAGES = ({% for code, name in languages %}
    ('{{ code }}', _('{{ name }}')),
{% endfor %})

ROOT_URLCONF = '{{ project_name }}.urls'

TEMPLATE_DIRS = (
    os.path.join(ROOT_DIR, 'templates'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'statirator.core.context_processors.st_settings'
)

LOCALE_PATHS = (
    os.path.join(ROOT_DIR, 'locale'),
)

# Static files setup
STATIC_URL = '/'
STATIC_ROOT = BUILD_DIR
STATICFILES_DIRS = (
    os.path.join(ROOT_DIR, 'static'),
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django_medusa',
    'taggit',
    'statirator.core',
    'statirator.blog',
    'statirator.pages',
)

MEDUSA_RENDERER_CLASS = "django_medusa.renderers.DiskStaticSiteRenderer"
MEDUSA_MULTITHREAD = False
MEDUSA_DEPLOY_DIR = BUILD_DIR

# Set your Analytics site id in here to enable analytics in pages
GOOGLE_ANALYTICS_ID = ''
