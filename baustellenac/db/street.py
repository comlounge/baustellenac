#encoding=utf8

from mongogogo import *
import datetime
import json

__all__=["Street", "StreetSchema", "Streets"]


class StreetSchema(Schema):
    """main schema for a street"""

    name = String()
    lat = Float()
    lng = Float()


class Street(Record):

    schema = StreetSchema()

    @property
    def latlng(self):
        #return json.dumps({'lat':self.lat, 'lng':self.lng})
        return [self.lat, self.lng]


class Streets(Collection):

    data_class = Street
    create_ids = True
