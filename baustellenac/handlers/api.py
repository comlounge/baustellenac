#encoding=utf8
from starflyer import asjson
from .. import BaseHandler


class AllSites(BaseHandler):
    """return all sites as full json objects"""

    @asjson()
    def get(self):
        """render the view"""
        baustellen = list(self.config.dbs.baustellen.active_sites)
        return [b.public_json for b in baustellen]
    post = get


class Site(BaseHandler):
    """show the impressum"""

    @asjson()
    def get(self, site_id):
        """render the view"""
        #print self.config.dbs.baustellen.get(site_id)
        #return self.config.dbs.baustellen.get(site_id)
        return {
            'site' : self.config.dbs.baustellen.get(site_id).public_json,
            'city_names' : self.config.cities
        }
    post = get
