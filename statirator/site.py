"Site definition"
import os

class Site(object):
    """Site object"""

    def __init__(self, root_dir='.', build_dir='_build',
            ignore_starting_with='_', templates_dir='_templates'):
        """Defines the basic site object"""

        self.root_dir = os.path.abspath(root_dir)
        self.build_dir = build_dir
        self.ignore_starting_with = ignore_starting_with
        self.templates_dir = templates_dir
