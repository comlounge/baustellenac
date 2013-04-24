#encoding=utf8

import pymongo

from .. import BaseHandler

class IndexView(BaseHandler):
    """an index handler"""

    template = "index.html"

    def get(self):
        """render the view"""
        return self.render(
            sites = self.config.dbs.baustellen.find(),
        )
    post = get

class Impressum(BaseHandler):
    """show the impressum"""

    template = "impressum.html"

    def get(self):
        """render the view"""
        return self.render()
