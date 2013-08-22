#encoding=utf8

from mongogogo import *
import datetime

__all__=["Organisation", "OrganisationSchema", "Organisations"]


class OrganisationSchema(Schema):
    """main schema for an organisation of a site (Träger)"""

    name = String()


class Organisation(Record):

    schema = OrganisationSchema()


class Organisations(Collection):

    data_class = Organisation
    create_ids = True
