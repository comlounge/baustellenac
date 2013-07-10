#encoding=utf8

import pymongo

from starflyer import asjson, redirect
from .. import BaseHandler
from forms import SiteForm


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

    def get(self):
        """render the view"""
        form = SiteForm(self.request.form)
        if self.request.method == 'POST' and form.validate():
            f = form.data
            site.update(f)
            self.config.dbs.baustellen.put(site)
            self.flash(self._(u"Baustellen %s aktualisiert" %site.name), category="info")
            return redirect(self.url_for("sites"))
        return self.render(
            form = form
        )
    post = get

class SiteEditView(BaseHandler):
    """shows and processes the site edit form"""

    template = "site_edit.html"

    def get(self, site_id):
        """render the view"""
        site = self.config.dbs.baustellen.get(site_id)
        form = SiteForm(self.request.form, obj=site)
        if self.request.method == 'POST' and form.validate():
            f = form.data
            site.update(f)
            self.config.dbs.baustellen.put(site)
            self.flash(self._(u"Baustellen %s aktualisiert" %site.name), category="info")
            return redirect(self.url_for("sites"))
        return self.render(
            site = site,
            form = form
        )
    post = get