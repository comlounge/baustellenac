# encoding=utf-8
import starflyer
from starflyer import redirect
import functools
import urllib
import wtforms
import werkzeug.exceptions
from functools import partial

from wtforms.ext.i18n.form import Form

__all__ = ["BaseForm", "BaseHandler", 'logged_in']

class logged_in(object):
    """check if a valid user is present"""

    def __call__(self, method):
        """check user"""
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            #import pdb; pdb.set_trace()
            #print self.user
            if self.user is None:
                redirect_url = self.url_for("userbase.login", force_external=True)
                came_from = urllib.quote_plus(self.request.url)
                self.flash(self._('Please log in.'), category="danger")
                return redirect('%s?came_from=%s' %(redirect_url, came_from))
            return method(self, *args, **kwargs)
        return wrapper


class BaseForm(Form):
    """a form which also carries the config object"""

    LANGUAGES = ['de', 'en']

    def __init__(self, formdata=None, obj = None, prefix='', config = None, app = None, **kwargs):
        super(BaseForm, self).__init__(formdata=formdata, obj=obj, prefix=prefix, **kwargs)
        self.config = config
        self.app = app


class BaseHandler(starflyer.Handler):
    """an extended handler """

    selected_action = None

    def before(self):
        """prepare the handler"""
        super(BaseHandler, self).before()

    @property
    def is_admin(self):
        """check for admin"""
        return True # TODO: do real check, e.g. checking apache header

    @property
    def render_context(self):
        """provide more information to the render method"""
        payload = dict(
            title = self.config.title,
            url = self.request.url,
            description = self.config.description,
            is_admin = self.is_admin,
        )
        return payload


