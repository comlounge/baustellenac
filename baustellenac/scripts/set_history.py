#coding: utf-8

import re
import time
import csv
import datetime
import requests

from geopy import geocoders

from starflyer.scripts import ScriptBase
from baustellenac.db import Street


class History(ScriptBase):
    """script to sync the userids with entries which have a profile set"""

    def __call__(self):
        for s in self.app.config.dbs.baustellen.find():
            s.edit_history = []
            self.app.config.dbs.baustellen.put(s)


def import_data():
    f = History()
    f()

if __name__=="__main__":
    import_data()
