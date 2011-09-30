"Site definition"
import os

class Site(object):
    """Site object"""

    def __init__(self, name='Default', root='.', source='source', build='build',
            ignore_starting_with='_'):
        """Defines the basic site object"""

        self.name = name
        self.root = os.path.abspath(root)
        self.source = source
        self.build = build
        self.ignore_starting_with = ignore_starting_with
