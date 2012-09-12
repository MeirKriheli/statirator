from django.conf.urls import patterns, url
from django.conf.urls.i18n import i18n_patterns
from statirator.blog.views import PostView


urlpatterns = patterns(
    '',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$',
        PostView.as_view(), name='blog_post'),
)

# make all the urls patterns again, with i18n translations, that way default
# language is not prefixed

urlpatterns += i18n_patterns(
    '',
    *[url(x._regex, x.callback, name='i18n_' + x.name) for x in urlpatterns]
)
