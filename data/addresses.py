#!/usr/bin/env python2
import os
import json
from urllib import urlencode
from urllib2 import urlopen

DIR = os.path.join('downloads', 'views')

def main():
    views = filter(lambda view: '.json' == view[-5:], os.listdir(DIR))
    for view in views:
        f = open(os.path.join(DIR, view))
        data = json.load(f)
        f.close()
        columns = {
            'address': list(address(data['columns'])),
            'description': list(description(data['columns'])),
        }

def column_names(columns):
    'Column names'
    return [column['name'] for column in columns]

def address(columns):
    'Get the address as a list of columns for geocoding.'
    streets = filter(lambda c: 'street' in c.lower() or 'address' in c.lower(), column_names(columns))
    zipcodes= filter(lambda c: 'zip' in c.lower(), column_names(columns))

    if len(streets) > 0:
        return streets[:1] + zipcodes[:1]
    else:
        return []

def is_description(column_name):
    for word in {'street', 'address', 'zip', 'date'}:
        if word in column_name.lower():
            return False
    else:
        return True

def description(columns):
    'Get a description as a list of columns for the pop-up box.'
    return filter(is_description, column_names(columns)) #[:3]



GEOCODE_URL = 'http://open.mapquestapi.com/nominatim/v1/search?format=json&%s'
def geocode(address):
    url = GEOCODE_URL % urlencode({'q': address + ', New York, NY'})
    print url
    handle = urlopen(url)
    d = json.load(handle)
    if len(d) > 0:
        return d[0]['lon'], d[0]['lat']
    else:
        return None

if __name__ == '__main__':
    print geocode('625 6th Avenue')
    exit(0)
    main()

