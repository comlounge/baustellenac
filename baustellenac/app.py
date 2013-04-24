# coding=utf-8

import pymongo
import pkg_resources

from starflyer import Application, URL, AttributeMapper

import re
from jinja2 import evalcontextfilter, Markup, escape

import handlers
import db

#
# custom jinja filters
#


_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
_striptags_re = re.compile(r'(<!--.*?-->|<[^>]*>)')

@evalcontextfilter
def nl2br(eval_ctx, value):
    value = _striptags_re.sub(' ', value)
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n')
                      for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

try:
    import simplejson as json
except ImportError:
    import json

if '\\/' not in json.dumps('/'):

    def _tojson_filter(*args, **kwargs):
        return json.dumps(*args, **kwargs).replace('/', '\\/')
else:
    _tojson_filter = json.dumps


###
### i18n
###

def get_locale(handler):
    return "de" # for now

###
### APP
###

class BaustellenApp(Application):
    """baustellen aachen application"""

    defaults = {
        'log_name'              : "baustellenapp",
        'server_name'           : "dev.localhost:9008",
        'title'                 : "Baustellen Aachen",
        'description'           : "Alle Baustellen in Aachen",
        #'debug'                 : False,
        'mongodb_name'          : "baustellenac",
        'mongodb_port'          : 27017,
        'mongodb_host'          : "localhost",
        'secret_key'            : "c987sd9cs7c98d7d&%$%&hhhs8c7zcbs87ct 987csd987csd9877stc 8c7cs8 78 7dts 8cs97tugjgjzGUZGUzgcdcg&%%$",
        'session_cookie_domain' : "dev.localhost",
    }

    betreiber = {
        1 : "Stadt Aachen",
        2 : "Aachener Stadtbetrieb",
        3 : "STAWAG",
        4 : "NetAachen"
    }

    modules = [
    ]

    jinja_filters = {
        'nl2br' : nl2br,
        'tojson' : _tojson_filter,
    }

    routes = [
        URL('/', 'index', handlers.index.IndexView),
        URL('/impressum.html', 'impressum', handlers.index.Impressum),
    ]

    def finalize_setup(self):
        """do our own configuration stuff"""
        self.config.dbs = AttributeMapper()
        mydb = self.config.dbs.db = pymongo.Connection(
            self.config.mongodb_host,
            self.config.mongodb_port
        )[self.config.mongodb_name]
        self.config.dbs.baustellen = db.Sites(mydb.sites, app=self, config=self.config)


def app(config, **local_config):
    """return the config"""
    return BaustellenApp(__name__, local_config)

