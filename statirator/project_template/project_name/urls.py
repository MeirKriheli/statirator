from django.conf.urls import patterns, url
from django.conf.urls.i18n import i18n_patterns
from statirator.blog import views


urlpatterns = patterns(
    '',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$',
        views.PostView.as_view(), name='blog_post'),
    url('r^archive/$', views.ArchiveView.as_view(), name='blog_archive')
)

# make all the urls patterns again, with i18n translations, that way default
# language is not prefixed

urlpatterns += i18n_patterns(
    '',
    *[url(x._regex, x.callback, name='i18n_' + x.name) for x in urlpatterns]
)
