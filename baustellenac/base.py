# encoding=utf-8
import starflyer
from starflyer import redirect
import functools
import wtforms
import werkzeug.exceptions
from functools import partial

from wtforms.ext.i18n.form import Form

__all__ = ["BaseForm", "BaseHandler", 'is_admin']

class is_admin(object):
    """ensure that the logged in user is an admin"""

    def __call__(self, method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            return method(self, *args, **kwargs)
            # TODO: do some simple admin check here
            self.flash(self._("You don't have the correct permissions to access this page."), category="error")
            return redirect(self.url_for("index"))
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


