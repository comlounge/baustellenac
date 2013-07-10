from .. import BaseHandler, logged_in


class Overview(BaseHandler):
    """an index handler"""

    template = "admin.html"

    @logged_in()
    def get(self):
        """render the view"""
        return self.render(
            sites = self.config.dbs.baustellen.find().sort("name", 1),
        )
    post = get
