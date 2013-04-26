#coding: utf-8

import re
import csv
import datetime
import requests

from starflyer.scripts import ScriptBase
from baustellenac.db import Site

#db = pymongo.Connection().baustellenac.data
osm_url = 'http://nominatim.openstreetmap.org/search?q=%s %s, Aachen&format=json&polygon=0&addressdetails=1'
gm_url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s+Aachen&sensor=false'

class ImportData(ScriptBase):
    """script to sync the userids with entries which have a profile set"""

    def __call__(self):
        filename = self.args.filename[0]
        with open(filename, 'rU') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for d in reader:
                if d['#'].strip():
                    organisation = unicode(d['Träger'], 'utf-8')
                    for i in range(2,5):
                        if d['Träger %d' %i] != '':
                            organisation = '%s/%s' %(organisation, d['Träger %d' %i])
                    site_data = {
                        'name' : unicode(d['Titel'], 'utf-8'),
                        'subtitle' : unicode(d['Untertitel'], 'utf-8'),
                        'description' : unicode(d['Beschreibung'], 'utf-8'),
                        'organisation' : organisation,
                        'approx_timeframe' : unicode(d['Datum_Text'], 'utf-8'),
                    }
                    if d['Start genau'].strip():
                        site_data['start_date'] = datetime.datetime.strptime(d['Start genau'], '%d.%m.%Y')
                    if d['Ende genau'].strip():
                        site_data['end_date'] = datetime.datetime.strptime(d['Ende genau'], '%d.%m.%Y')

                    sections = self.get_sections(d)
                    if len(sections) > 0:
                        site_data['sections'] = self.get_sections(d)
                        site = Site(site_data)
                        del site['_id']
                        self.app.config.dbs.baustellen.save(site)


    def get_sections(self, d):
        sections = []
        streets_string = d['Strassen']

        # check for sub_streets (intersections)
        sub_streets = []
        if '(' in streets_string:
            s_match = re.search(r'\((.*?)\)', streets_string)
            sub_streets = s_match.group(1).split(',')
            streets_string = streets_string.replace(s_match.group(0), '')
        streets = [{'name':s, 'number':[]} for s in streets_string.strip().split(',')]

        if len(sub_streets) > 0:
            latlngs = []
            #for ss in sub_streets:
            #    query = '%s+and+%s' %(streets[0]['name'], ss.strip())
            #    url = gm_url %query
            #    data = requests.get(url).json()
            #    if len(data['results']) > 0:
            #        latlngs.append(data['results'][0]['geometry']['location'])

            section = {
                'street'       : unicode(streets[0]['name'], 'utf-8'),
                'city'         : u'Aachen',
                'zip'          : u'52064', # TODO: determine correct ZIP
                #'start_lat'    : latlngs[0]['lat'],
                #'start_lng'    : latlngs[0]['lng'],
            }
            start_latlng = self.get_gm_latlng(streets[0]['name'])
            if start_latlng is not None:
                section['start_lat'] = start_latlng['lat']
                section['start_lng'] = start_latlng['lng']
            sections.append(section)

        else:
            #return []
            for s in streets:
                # check for streetnumbers
                n_match = re.search(r'([0-9]+(\s*(-|/)*\s*[0-9]+)*)', s['name'])
                if n_match is not None:
                    s['name'] = s['name'].replace(n_match.group(0), '').strip()
                    numbers_string = n_match.group(1).replace(' ', '').replace('/', '-')
                    numbers = numbers_string.split('-')
                    if len(numbers) > 1:
                        if numbers[0] == '':
                            numbers[0] = '1'
                        if numbers[1] == '':
                            numbers[1] = '99999'
                    s['number'] = numbers
                else:
                    s['number'] = ['1', '99999']

                # create sections
                section = {
                    'street'       : unicode(s['name'], 'utf-8'),
                    'city'         : u'Aachen',
                    'zip'          : u'52064', # TODO: determine correct ZIP
                }
                start_latlng = self.get_gm_latlng(s['name'], s['number'][0])
                if start_latlng is not None:
                    section['start_lat'] = start_latlng['lat']
                    section['start_lng'] = start_latlng['lng']
                if len(s['number']) > 1:
                    section['end_number'] = s['number'][1]
                    end_latlng = self.get_gm_latlng(s['name'], s['number'][1])
                    if end_latlng is not None:
                        section['end_lat'] = end_latlng['lat']
                        section['end_lng'] = end_latlng['lng']

                sections.append(section)

        return sections

        #for s in d['Strassen'].split(','):
        #
        #print streets

    def get_gm_latlng(self, street, number=None):
        query = street
        if number is not None:
            query = '%s+%s' %(query,number)
        url = gm_url %query
        data = requests.get(url).json()
        if len(data['results']) > 0:
            return data['results'][0]['geometry']['location']
        return None

    def get_osm_latlng(self, street, number=None):
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
    f.app.config.dbs.baustellen._remove()
    f()

if __name__=="__main__":
    importdata()
