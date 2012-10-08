from __future__ import print_function

import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.template.base import TemplateDoesNotExist
from django.template.loader import find_template_loader


class Command(BaseCommand):

    help = "Copy a template into templates dir to override and extend it"
    args = "<template_name template_name ...>"

    def handle(self, *args, **options):
        if not args:
            raise CommandError('Please specify at least one template name')

        loaders = []
        for loader_name in settings.TEMPLATE_LOADERS:
            loader = find_template_loader(loader_name)
            if loader is not None:
                loaders.append(loader)

        # make sure we have the loaders
        for name in args:
            source = display_name = None
            for loader in loaders:
                try:
                    source, display_name = loader.load_template_source(name, None)
                except TemplateDoesNotExist:
                    pass

            if source is None:
                raise CommandError('Template {0} not found'.format(name))

            full_name = os.path.abspath(
                os.path.join(settings.TEMPLATE_DIRS[0], name))

            head, tail = os.path.split(full_name)

            if head:
                try:
                    os.makedirs(head)
                except OSError:
                    pass

            with open(full_name, 'w') as tmpl:
                tmpl.write(source)

            print('Copied template {0}'.format(name))
