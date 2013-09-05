#encoding=utf8

import pymongo
import datetime
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
        form = SiteForm(self.request.form)
        organisations = [(o.name,o.name) for o in self.config.dbs.traeger.find().sort('name')]
        form.organisation.choices = organisations
        form.city.choices = [(k,v) for k,v in self.config.cities.items()]
        if self.request.method == 'POST' and form.validate():
            f = form.data
            site_data = {}
            site_data.update(f)
            site_data['edit_history'] = [{'user':self.user['username'], 'date':datetime.datetime.now()}]
            site = db.Site(site_data)
            del site['_id']
            self.config.dbs.baustellen.put(site)
            self.flash(self._(u"Baustellen %s erfolgreich angelegt" %site.name), category="info")
            return redirect(self.url_for("admin_overview"))
        return self.render(
            form = form,
            streets = self.config.dbs.streets.find().sort('name')
        )
    post = get

class SiteEditView(BaseHandler):
    """shows and processes the site edit form"""

    template = "site_edit.html"

    @logged_in()
    def get(self, site_id):
        """render the view"""
        site = self.config.dbs.baustellen.get(site_id)
        form = SiteForm(self.request.form, obj=site)
        organisations = [(o.name,o.name) for o in self.config.dbs.traeger.find().sort('name')]
        form.organisation.choices = organisations
        form.city.choices = [(k,v) for k,v in self.config.cities.items()]
        if self.request.method == 'POST' and form.validate():
            f = form.data
            site.update(f)
            site.edit_history.append({'user':self.user['username'], 'date':datetime.datetime.now()})
            self.config.dbs.baustellen.put(site)
            self.flash(self._(u"Baustellen %s aktualisiert" %site.name), category="info")
            return redirect(self.url_for("admin_overview"))
        return self.render(
            site = site,
            form = form,
            streets = self.config.dbs.streets.find()
        )
    post = get

class SiteRemoveView(BaseHandler):
    """processes a delete request vie post calledby ajax"""

    @logged_in()
    def post(self, site_id):
        """render the view"""
        site = self.config.dbs.baustellen.get(site_id)
        try:
            self.config.dbs.baustellen.remove(site)
            self.flash(self._(u"Baustelle <i>%s</i> erfolgreich gelöscht" %site.name), category="info")
        except:
            self.flash(self._(u"Baustelle <i>%s</i> konnte nicht gelöscht werden" %site.name), category="danger")
        return redirect(self.url_for("admin_overview"))