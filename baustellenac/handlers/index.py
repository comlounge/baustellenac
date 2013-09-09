#encoding=utf8

import pymongo
from datetime import datetime

from .. import BaseHandler

class IndexView(BaseHandler):
    """an index handler"""

    template = "index.html"

    def get(self):
        """render the view"""
        now = datetime.now()
        return self.render(
            sites = self.config.dbs.baustellen.find({'start_date':{'$lte':now}, 'end_date':{'$gte':now}}).sort("name", 1),
        )
    post = get

class Impressum(BaseHandler):
    """show the impressum"""

    template = "impressum.html"

    def get(self):
        """render the view"""
        return self.render()
