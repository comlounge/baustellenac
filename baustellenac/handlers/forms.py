#encoding=utf8
import json
import decimal

from .. import BaseForm

from wtforms import TextField, PasswordField, FieldList, BooleanField, IntegerField, DecimalField
from wtforms import SelectField, DateField, TextAreaField, HiddenField, FloatField, Field, FormField, Form
from wtforms import validators as v
from wtforms.widgets import html_params, HTMLString, TextInput, HiddenInput, Select
from jinja2 import Template

###
### CUSTOM WIDGETS etc.
###


def checkbox_button(field, **kwargs):
    """custom wtforms widget for the checkbox button toggle stuff"""
    kwargs.setdefault('type', 'checkbox')
    value = field.data
    field_id = kwargs.pop('id', field.id)
    button_id = "%s-%s" %(field_id, field_id)
    hidden_params = {
        'type' : 'hidden',
        'id' : field_id,
        'name' : field.name,
        'value' : "1" if value else "0"
    }
    button_params = {
        'id' : button_id,
        'for' : field_id,
    }
    if value:
        button_params['class'] = "btn btn-toggle active"
    else:
        button_params['class'] = "btn btn-toggle"
    if "class" in kwargs:
        button_params['class'] = button_params['class'] + " " + kwargs['class']

    html = [
        u'<input %s />' %html_params(**hidden_params),
        u'<button %s >' %html_params(**button_params)
    ]
    if value:
        html.append(u'<i class="icon icon-ok icon-nok"></i> ')
    else:
        html.append(u'<i class="icon icon-nok"></i> ')
    html.append(field.label.text)
    html.append(u"</button>")
    return u''.join(html)


class BooleanValueField(Field):
    """
    Represents an checkbox button
    """
    widget = checkbox_button

    def __init__(self, label=None, validators=None, **kwargs):
        super(BooleanValueField, self).__init__(label, validators, **kwargs)

    def process_data(self, value):
        self.data = bool(value)

    def process_formdata(self, valuelist):
        # Checkboxes and submit buttons simply do not send a value when
        # unchecked/not pressed. So the actual value="" doesn't matter for
        # purpose of determining .data, only whether one exists or not.
        self.data = valuelist[0] == u"1"

    def _value(self):
        if self.raw_data:
            return unicode(self.raw_data[0])
        else:
            return u'y'

class JSONField(Field):
    """a JSON field"""

    def _value(self):
        if self.data:
            return json.dumps(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist and len(valuelist)>0:
            self.data = json.loads(valuelist[0])
        else:
            self.data = u""

class SelectWithPlaceholder(Select):

    def __init__(self, multiple=False, placeholder=None):
        self.multiple = multiple
        self.placeholder = placeholder

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if self.multiple:
            kwargs['multiple'] = True
        html = ['<select %s>' % html_params(name=field.name, **kwargs)]
        if self.placeholder is not None:
            html.append('<option disabled selected style="display:none">%s</option>' % self.placeholder)
        for val, label, selected in field.iter_choices():
            html.append(self.render_option(val, label, selected))
        html.append('</select>')
        return HTMLString(''.join(html))

class DatePickerWidget(TextInput):

    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'date-picker %s' % c
        return super(DatePickerWidget, self).__call__(field, **kwargs)


class SiteForm(BaseForm):
    """a client form"""

    name = TextField(u"Name", default="")
    subtitle = TextField(u"zusätzl. Titel", default="")
    description = TextField(u"Beschreibung", default="")
    #organisation = TextField(u"Träger", default="")
    organisation = SelectField(u"Träger", choices=[], widget=SelectWithPlaceholder(placeholder=u"Wählen Sie einen Träger..."))
    sidewalk_only = BooleanField(u"Nur auf dem Gehweg?")
    name = TextField(u"Name", default="")
    start_date = DateField(u"Start", format='%d.%m.%Y', widget=DatePickerWidget()) # start date of project
    end_date = DateField(u"Ende", format='%d.%m.%Y', widget=DatePickerWidget()) # approx. end date of project
    approx_timeframe = TextField(u"ungefährer Zeitraum", default="")
    lat = HiddenField(default='')
    lng = HiddenField(default='')
    polyline = JSONField(u'Polyline', default={}, widget=HiddenInput())
