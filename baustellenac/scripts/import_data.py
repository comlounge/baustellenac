#coding: utf-8

import csv
import datetime
import requests

from starflyer.scripts import ScriptBase
from baustellenac.db import Site

#db = pymongo.Connection().baustellenac.data
osm_url = 'http://nominatim.openstreetmap.org/search?q=%s %s, Aachen&format=json&polygon=0&addressdetails=1'

class ImportData(ScriptBase):
    """script to sync the userids with entries which have a profile set"""

    def __call__(self):
        filename = self.args.filename[0]
        with open(filename, 'rU') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for d in reader:
                if d['#'].strip():
                    site_data = {
                        'name' : unicode(d['Titel'], 'utf-8'),
                        'description' : unicode(d['Beschreibung'], 'utf-8'),
                        'organisation' : u'%s/%s' %(d['Träger'], d['Träger 2']),
                        'start_date' : datetime.datetime.strptime(d['Start genau'], '%d.%m.%Y'),
                        'end_date' : datetime.datetime.strptime(d['Ende genau'], '%d.%m.%Y'),
                        'approx_timeframe' : u'%s - %s' %(d['Start text'], d['Ende text']),
                    }

                    start_street = unicode(d['von Strasse'], 'utf-8')
                    end_street = unicode(d['bis Strasse'], 'utf-8') if d['bis Strasse'].strip() else start_street
                    start_number = d['von HNR']
                    end_number = unicode(d['bis HNR'], 'utf-8') if d['bis HNR'].strip() else unicode(d['von HNR'], 'utf-8')
                    section = {
                        'start_street' : start_street,
                        'end_street'   : end_street,
                        'start_number' : start_number,
                        'end_number'   : end_number,
                        'city'         : u'Aachen',
                        'zip'          : u'52064', # TODO: determine correct ZIP
                    }

                    section['start_lat'], section['start_lng'] = self.get_latlng(start_street, start_number)
                    section['end_lat'], section['end_lng'] = self.get_latlng(end_street, end_number)
                    site_data['sections'] = [section]

                    site = Site(site_data)
                    self.app.config.dbs.baustellen.save(site)


    def get_latlng(self, street, number):
        url = osm_url %(street, number)
        data = requests.get(url).json()
        if len(data) > 0:
            return (data[0]['lat'], data[0]['lon'])
        return (None, None)

    def extend_parser(self):
        """add the location of the file to the parser"""
        self.parser.add_argument('filename', metavar='FILE', nargs=1, help='the csv file to read')


def importdata():
    f = ImportData()
    f()

if __name__=="__main__":
    f = ImportData()
    f()
