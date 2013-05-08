from __future__ import print_function

import codecs
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils import translation
from optparse import make_option

from statirator.blog.utils import get_blog_dir


class Command(BaseCommand):

    args = '<english title or slug>'
    help = 'Create a new rst blog post'

    option_list = (
        make_option(
            '--draft', '-d', dest='draft', default=False, action='store_true',
            help='Is is a draft (unpublished) ? [Default: "%default"]'),
    ) + BaseCommand.option_list

    def handle(self, *args, **options):

        if len(args) != 1:
            raise CommandError('Single argument of English title or slug '
                               'is required')

        title_or_slug = args[0]
        slug = slugify(title_or_slug)
        draft = int(options['draft'])

        ctx = {
            'slug': slug,
            'draft': draft,
        }

        filename = os.path.join(get_blog_dir(), slug + '.rst')

        if os.path.exists(filename):
            raise CommandError('"{0}" exists, aborting'.format(filename))
        with codecs.open(filename, 'w', 'utf-8') as post_file:

            meta_rendered = render_to_string('blog/new_post_metadata.txt', ctx)
            post_file.write(meta_rendered)

            cur_lang = translation.get_language()

            # now we need to render for each language
            for lang_code, lang_name in settings.LANGUAGES:
                post_file.write('\n.. --')
                translation.activate(lang_code)

                ctx.update({'title': title_or_slug})
                rendered = render_to_string('blog/new_post_content.txt', ctx)
                post_file.write(rendered)

            translation.activate(cur_lang)

        print("Created post", os.path.relpath(filename))
