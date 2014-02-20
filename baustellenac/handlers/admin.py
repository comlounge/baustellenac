#encoding=utf8

from datetime import datetime

from starflyer import asjson

from .. import BaseHandler, logged_in
from forms import SiteForm, SiteFilterForm
from baustellenac import db


class Overview(BaseHandler):
    """an index handler"""

    template = "admin.html"

    @logged_in()
    def get(self):
        """render the view"""
        filter_form = SiteFilterForm(self.request.args)
        filter_form.city.choices = [('all', 'alle')] + self.config.dbs.baustellen.get_distinct_cities_tuple()
        query = self.request.args.to_dict()
        if query.get('city', '') == 'all':
            del query['city']
        if query.has_key('show_old_sites'):
            del query['show_old_sites']
        else:
            query['end_date'] = {'$gte':datetime.now()}
        return self.render(
            form = filter_form,
            sites = self.config.dbs.baustellen.find(query).sort("name"),
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

