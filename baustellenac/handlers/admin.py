#encoding=utf8

from starflyer import asjson

from .. import BaseHandler, logged_in
from forms import SiteForm
from baustellenac import db


class Overview(BaseHandler):
    """an index handler"""

    template = "admin.html"

    @logged_in()
    def get(self):
        """render the view"""
        return self.render(
            sites = self.config.dbs.baustellen.find().sort("name"),
        )
    post = get


class OrganisationAdd(BaseHandler):
    """add an organisation"""

    @logged_in()
    @asjson()
    def post(self):
        """render the view"""
        f = self.request.form
        organisation = db.Organisation(f)
        self.config.dbs.traeger.put(organisation)
        self.flash(self._(u"Träger %s hinzugefügt" %organisation.name), category="info")
        return {'status' : 'ok', 'name' : organisation.name}

