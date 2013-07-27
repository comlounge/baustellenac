from mongogogo import *
import datetime

__all__=["Site", "SiteSchema", "Sites"]

class BaseError(Exception):
    """base class for exceptions"""

    def __init__(self, msg):
        """initialize the error with a message"""
        self.msg = msg

class WorkflowError(BaseError):
    """error in workflow e.g. transition not allowed"""

    def __init__(self, msg = u"Transition nicht erlaubt" , old_state = None, new_state = None):
        """initialize the error with a message"""
        self.msg = msg
        self.old_state = old_state
        self.new_state = new_state

    def __str__(self):
        """return a printable representation"""
        return """<WorkflowError: %s (old=%s, new=%s)>""" %(self.msg, self.old_state, self.new_state)

class SectionSchema(Schema):
    """a location described by name, lat and long"""
    street = String()
    city = String()
    zip = String()
    start_lat = Float()
    start_lng = Float()
    end_lat = Float()
    end_lng = Float()

class LatLngSchema(Schema):
    lat = Float()
    lng = Float()

class SiteSchema(Schema):
    """main schema for a street construction site"""

    created             = DateTime()
    updated             = DateTime()
    workflow            = String(required = True, default = "created")

    # base data
    name                = String(required = False) # project name or something like that
    subtitle            = String(required = False) # project name or something like that
    description         = String(required = False) # long description if given
    organisation        = String() # who is doing this?
    sidewalk_only       = Boolean() # is this on a sidewalk only?

    # these field define when to show it on the map
    start_date          = DateTime() # start date of project
    end_date            = DateTime() # approx. end date of project

    # this field describes an approx. time frame in plain text
    approx_timeframe    = String()

    # where the icon is positioned
    lat                 = String()
    lng                 = String()

    # the drawable line
    polyline            = List(LatLngSchema())

    # shows if we have exact lat/lng
    exact_position = Boolean()

    sections            = List(SectionSchema()) # list of sections/streets. Only one if it's only one location

class Site(Record):

    schema = SiteSchema()


class Sites(Collection):

    data_class = Site
    create_ids = True
