#coding: utf-8

import re
import time
import csv
import datetime
import requests

from starflyer.scripts import ScriptBase
from baustellenac.db import Organisation


class ImportData(ScriptBase):
    """script to sync the userids with entries which have a profile set"""

    def __call__(self):
        filename = self.args.filename[0]
        with open(filename, 'rU') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for d in reader:
                if d['#'].strip():
                    organisation = unicode(d['Träger'], 'utf-8')
                    test = self.app.config.dbs.traeger.find({'name':organisation})
                    if test.count() == 0:
                        o = Organisation({'name':organisation})
                        self.app.config.dbs.traeger.put(o)
                    #print organisation

    def extend_parser(self):
        """add the location of the file to the parser"""
        self.parser.add_argument('filename', metavar='FILE', nargs=1, help='the csv file to read')


def import_data():
    f = ImportData()
    f()

if __name__=="__main__":
    import_data()
