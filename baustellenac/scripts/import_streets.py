#coding: utf-8

import re
import time
import csv
import datetime
import requests

from geopy import geocoders

from starflyer.scripts import ScriptBase
from baustellenac.db import Street


class ImportData(ScriptBase):
    """script to sync the userids with entries which have a profile set"""

    def __init__(self, *args, **kwargs):
        super(ImportData, self).__init__(*args, **kwargs)
        self.geocoder = geocoders.GoogleV3()

    def __call__(self):
        filename = self.args.filename[0]
        with open(filename, 'rU') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for d in reader:
                streets_string = d['Strassen']
                streets = [{'name':unicode(s.strip(),'utf-8')} for s in streets_string.strip().split(',')]
                for sn in streets:
                    lat, lng = self.get_geo_data(sn['name'])
                    sn['lat'] = lat
                    sn['lng'] = lng
                    test = self.app.config.dbs.streets.find(sn)
                    if test.count() == 0 and sn['name']!='':
                        s = Street(sn)
                        self.app.config.dbs.streets.put(s)

    def get_geo_data(self, addr):
        place, (lat, lng) = self.geocoder.geocode(addr+", Aachen", exactly_one=False)[0]
        return (lat, lng)

    def extend_parser(self):
        """add the location of the file to the parser"""
        self.parser.add_argument('filename', metavar='FILE', nargs=1, help='the csv file to read')


def import_data():
    f = ImportData()
    f()

if __name__=="__main__":
    import_data()

"""
    #coding:utf-8
    import sys, os, time
    from django.core.management import setup_environ
    sys.path.append(os.path.abspath('%s/../..' % os.path.abspath(__file__)))
    try:
        import settings # Assumed to be in the same directory.
    except ImportError:
        sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
        sys.exit(1)

    project_directory = setup_environ(settings)
    project_name = os.path.basename(project_directory)
    os.environ['DJANGO_SETTINGS_MODULE'] = "%s.settings" % project_name


    from djangotest.geocoder import Geocoder
    from djangotest.polls.models import Denkmal, Land


    if __name__ == "__main__":
        denkmale = Denkmal.objects.filter(active=1,latitude__isnull=True,longitude__isnull=True)
        print len(denkmale)
        errors = {'unicode':0,
                  'value':0,
                  'other':0}
        for d in denkmale:
            print '============================================================='
            gc = Geocoder(d.stadt, d.plz, d.street)
            lat, lng = gc.get_geo_data()
            d.latitude = float(lat)
            d.longitude = float(lng)
            print '%s, %s, %s, %s' % (d.land.name.encode('utf-8'), d.kreis.name.encode('utf-8'), d.stadt.name.encode('utf-8'), d.name.encode('utf-8'))
            print lat,lng
            d.save()
            errors.update(gc.errors)




            #coding:utf-8
            import time
            from geopy import geocoders


            class Geocoder(object):

                def __init__(self, stadt, plz, street):
                    self.street = street
                    self.plz = plz
                    self.stadt = stadt
                    #self.coder = geocoders.Yahoo('dj0yJmk9TjdMYlM4NWl6a2FzJmQ9WVdrOWREQkdTRGx5TjJrbWNHbzlNVGt3TkRFeU5qWXkmcz1jb25zdW1lcnNlY3JldCZ4PTRm')
                    #self.coder = geocoders.Google()
                    self.coder = geocoders.GoogleV3()
                    self.errors = {'unicode':0,'value':0,'other':0}

                def get_geo_data(self):
                    lat = None
                    lng = None
                    addr = u"%s, %s %s, Germany" % (self.street, self.plz, self.stadt)
                    addr = addr.encode('utf-8')
                    try:
                        for place, (ylat, ylng) in self.coder.geocode(addr, exactly_one=False):
                            lat =  float(ylat)
                            lng = float(ylng)
                            break
                    except UnicodeEncodeError:
                        print addr
                        raise
                        self.errors['unicode'] += 1
                    except ValueError:
                        print addr
                        #raise
                        self.errors['value'] += 1
                    except:
                        addr = u"%s %s, Germany" % (self.plz, self.stadt)
                        try:
                            for place, (ylat, ylng) in self.coder.geocode(addr, exactly_one=False):
                                lat = float(ylat)
                                lng = float(ylng)
                                break
                        except:
                            print addr
                            raise
                        self.errors['other'] += 1

                    time.sleep(0.5)
                    return lat,lng






#coding:utf-8
import sys, os, time
from django.core.management import setup_environ
sys.path.append(os.path.abspath('%s/../..' % os.path.abspath(__file__)))
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

project_directory = setup_environ(settings)
project_name = os.path.basename(project_directory)
os.environ['DJANGO_SETTINGS_MODULE'] = "%s.settings" % project_name


from djangotest.geocoder import Geocoder
from djangotest.polls.models import Denkmal, Land


if __name__ == "__main__":
    denkmale = Denkmal.objects.filter(active=1,latitude__isnull=True,longitude__isnull=True)
    print len(denkmale)
    errors = {'unicode':0,
              'value':0,
              'other':0}
    for d in denkmale:
        print '============================================================='
        gc = Geocoder(d.stadt, d.plz, d.street)
        lat, lng = gc.get_geo_data()
        d.latitude = float(lat)
        d.longitude = float(lng)
        print '%s, %s, %s, %s' % (d.land.name.encode('utf-8'), d.kreis.name.encode('utf-8'), d.stadt.name.encode('utf-8'), d.name.encode('utf-8'))
        print lat,lng
        d.save()
        errors.update(gc.errors)
"""