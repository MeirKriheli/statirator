from django.conf.urls import patterns, url
from django.conf.urls.i18n import i18n_patterns
from statirator.blog import views, feeds
from statirator.pages import views as pviews


urlpatterns = patterns(
    '',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$',
        views.PostView.as_view(), name='blog_post'),
    url(r'^archive/$', views.ArchiveView.as_view(), name='blog_archive'),
    url(r'^blog\.rss$', feeds.PostsFeed(), name='blog_feed'),
    url(r'^tags/$', views.TagsView.as_view(), name='blog_tags'),
    url(r'^tags/(?P<slug>[-\w]+)/$', views.TagView.as_view(), name='blog_tag'),
    url(r'^tags/(?P<slug>[-\w]+)/tag.rss$', feeds.TagFeed(),
        name='blog_tag_feed'),
    url(r'^$', pviews.PageView.as_view(), {'slug': 'index'}, name='pages_index'),
)

# make all the urls patterns again, with i18n translations, that way default
# language is not prefixed

urlpatterns += i18n_patterns(
    '',
    *[url(x._regex, x.callback, x.default_args, name='i18n_' + x.name)
        for x in urlpatterns]
)
