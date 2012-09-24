from __future__ import print_function, absolute_import

from django.template.defaultfilters import slugify
from statirator.core.utils import find_files
from statirator.core.parsers import parse_rst
from .utils import get_blog_dir
from .models import I18NTag, Post


def rst_reader():
    "Finds rst posts, parses them and loads into the db."

    for post in find_files(get_blog_dir(), ['.rst']):
        print('Processing {0}'.format(post))
        with open(post) as p:
            parsed = parse_rst(p.read())

            generic_metadata, title, content = parsed.next()

            # got those, now go over the languages
            for metadata, title, content in parsed:
                lang = metadata['lang']

                tags = []
                for meta_tag in metadata['tags']:
                    try:
                        name, slug = meta_tag.split('|')
                    except ValueError:
                        name, slug = meta_tag, slugify(meta_tag)

                    i18n_slug = '{0}-{1}'.format(lang, slug)

                    tag, created = I18NTag.objects.get_or_create(
                        slug=i18n_slug, language=lang,
                        defaults={'name': name, 'slug_no_locale': slug})

                    if not created:
                        tag.name = name
                        tag.slug_no_locale = slug
                        tag.save()

                    tags.append(tag)

                defaults = dict(
                    title=title,
                    is_published=not generic_metadata['draft'],
                    content=content,
                    pubdate=generic_metadata['datetime'],
                    language=lang,
                    excerpt=metadata.get('excerpt'),
                    image=generic_metadata.get('image'))

                post, created = Post.objects.get_or_create(
                    slug=generic_metadata['slug'], defaults=defaults)

                if not created:
                    for field, val in defaults.iteritems():
                        setattr(post, field, val)
                    post.save()

                post.tags.set(*tags)

READERS = [rst_reader]
