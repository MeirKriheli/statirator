from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string


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
        metadata_rendered = render_to_string('blog/new_post_metadata.rst', ctx)
        print metadata_rendered
