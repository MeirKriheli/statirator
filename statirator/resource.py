"Resources for the database"""

import os

class Resource(object):
    """Reperents the default resource, copied verbatim"""

    resource_type = None
    resource_ext = None

    def __init__(self, app, folder, filename, language=None):
        self.folder = folder
        self.filename = filename
        self.app = None
        self.language = None

    def create_target_dir(self):
        pass
        
    def handle_resource(self):
        pass

class HtmlResource(Resource):
    """html template resource"""

    resource_type = 'html'
    resource_ext = 'html'
