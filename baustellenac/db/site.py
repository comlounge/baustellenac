from mongogogo import *
import datetime
import types

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

class LatLngListSchema(Schema):
    latlngs = List(LatLngSchema())

class EditSchema(Schema):
    user = String()
    date = DateTime()

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
    city                = String()
    sidewalk_only       = Boolean() # is this on a sidewalk only?

    # these field define when to show it on the map
    start_date          = DateTime() # start date of project
    end_date            = DateTime() # approx. end date of project

    # this field describes an approx. time frame in plain text
    approx_timeframe    = String()

    # where the icon is positioned
    lat                 = String()
    lng                 = String()

    # the drawable lines
    #polyline            = List(LatLngSchema(), required = False)
    polylines           = List(List(LatLngSchema()), required = False)
    #polylines           = List(LatLngListSchema(), required = False)

    # shows if we have exact lat/lng
    exact_position = Boolean()

    # editor history
    edit_history = List(EditSchema(), default=[])

    #sections            = List(SectionSchema()) # list of sections/streets. Only one if it's only one location

class Site(Record):

    schema = SiteSchema()
    _protected = ['schema', 'collection', '_protected', '_schemaless', 'default_values', 'workflow_states', 'initial_workflow_state', 'public_fields']
    initial_workflow_state = "created"
    default_values = {
        'created'       : datetime.datetime.utcnow,
        'updated'       : datetime.datetime.utcnow,
    }

    public_fields = [
        'city',
        'subtitle',
        'description',
        'organisation',
        'start_date',
        'end_date',
        'exact_position',
        'approx_timeframe',
        'approx_timeframe',
        'lat',
        'lng',
        'sidewalk_only',
        '_id',
        'name',
    ]

    def set_workflow(self, new_state):
        """set the workflow to a new state"""
        old_state = self.workflow
        if old_state is None:
            old_state = self.initial_workflow_state
        allowed_states = self.workflow_states[old_state]

        # check if transition is allowed
        if hasattr(self, "check_wf_"+new_state):
            m = getattr(self, "check_wf_"+new_state)
            if not m(old_state = old_state): # this should raise WorkflowError if not allowed otherwise return True
                raise WorkflowError(old_state = old_state, new_state = new_state) # fallback

        if new_state not in allowed_states:
            raise WorkflowError(old_state = old_state, new_state = new_state)

        # Trigger
        if hasattr(self, "on_wf_"+new_state):
            m = getattr(self, "on_wf_"+new_state)
            m(old_state = old_state)
        self.workflow = new_state


    @property
    def public_json(self):
        """return a public representation of the site"""
        data = {}
        for a,v in self.items():
            if a not in self.public_fields:
                continue
            # convert to utf8 if possible
            if type(v) == types.UnicodeType:
                v = v
                v = v.encode("utf-8")
                print a,type(v), v
            data[a] = v
        #data = dict([(a,v) for a,v in self.items() if a in self.public_fields])
        # add last updated field
        if self.edit_history is not None and len(self.edit_history)>0:
            last_updated = self.edit_history[-1]['date']
        else:
            last_updated = datetime.datetime(2013,1,1) # dummy date
        data['last_updated'] = last_updated
        return dict(data)


class Sites(Collection):

    data_class = Site
    create_ids = True

    @property
    def active_sites(self):
        now = datetime.datetime.now()
        return self.find({'start_date':{'$lte':now}, 'end_date':{'$gte':now}}).sort("name", 1)
