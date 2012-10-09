from django.conf.urls import patterns, url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from statirator.blog import views, feeds
from statirator.pages import views as pviews, sitemap as psitemap
from statirator.blog import sitemap as bsitemap

# we need to make sure the pages slug won't catch the /en/ etc  for index pages
# in various languages
langs_re = '|'.join(x[0] for x in settings.LANGUAGES)

sitemaps = {
    'pages': psitemap.PagesSiteMap,
    'blog': bsitemap.BlogSiteMap,
}

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
    # keep those last
    url(r'^$', pviews.PageView.as_view(), {'slug': 'index'}, name='pages_index'),
    url(r'^(?P<slug>(?!%s)[-\w]+)/$' % langs_re, pviews.PageView.as_view(),
        name='pages_page'),
)

# make all the urls patterns again, with i18n translations, that way default
# language is not prefixed

urlpatterns += i18n_patterns(
    '',
    *[url(x._regex, x.callback, x.default_args, name='i18n_' + x.name)
        for x in urlpatterns]
)

urlpatterns += patterns('django.contrib.sitemaps.views',
    url(r'^sitemap.xml$', 'sitemap', {'sitemaps': sitemaps}, name='sitemap'),
)
