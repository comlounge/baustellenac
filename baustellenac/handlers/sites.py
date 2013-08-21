#encoding=utf8

import pymongo
import uuid
import json

from starflyer import asjson, redirect
from .. import BaseHandler, logged_in
from forms import SiteForm
from baustellenac import db


class SitesView(BaseHandler):
    """list all sites"""

    template = "sites.html"

    def get(self):
        """render the view"""
        return self.render(
            sites = self.config.dbs.baustellen.find().sort("name", 1),
        )
    post = get

class SiteAddView(BaseHandler):
    """shows and processes the site edit form"""

    template = "site_add.html"

    @logged_in()
    def get(self):
        """render the view"""
        form = SiteForm()
        return self.render(
            form = form
        )

    @logged_in()
    def post(self):
        """save site"""
        form = SiteForm(self.request.form)
        if form.validate():
            f = form.data
            site_data = {}
            site_data.update(f)
            site = db.Site(site_data)
            del site['_id']
            self.config.dbs.baustellen.put(site)
            self.flash(self._(u"Baustellen %s erfolgreich angelegt" %site.name), category="info")
            return redirect(self.url_for("admin_overview"))
        return self.render(
            form = form
        )

class SiteEditView(BaseHandler):
    """shows and processes the site edit form"""

    template = "site_edit.html"

    @logged_in()
    def get(self, site_id):
        """render the view"""
        site = self.config.dbs.baustellen.get(site_id)
        form = SiteForm(self.request.form, obj=site)
        if self.request.method == 'POST' and form.validate():
            f = form.data
            site.update(f)
            self.config.dbs.baustellen.put(site)
            self.flash(self._(u"Baustellen %s aktualisiert" %site.name), category="info")
            return redirect(self.url_for("admin_overview"))
        return self.render(
            site = site,
            form = form
        )
    post = get