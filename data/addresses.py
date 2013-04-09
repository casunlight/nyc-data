#!/usr/bin/env python2
import os
import re
import json
from urllib import urlencode
from cache import get
from read_csv import read_csv

VIEWS_DIR   = os.path.join('downloads', 'views')
ROWS_DIR    = os.path.join('downloads', 'rows')
GEOJSON_DIR = os.path.join('downloads', 'geojson')

ANNOYING = re.compile(r'[^a-zA-Z]')
LATLNG = re.compile(r'\(([0-9][0-9].[0-9]+), (-[0-9][0-9].[0-9]+)\)')

from random import sample
sxx4_xhzg = [tuple(map(float, [row['Longitude'], row['Latitude']])) for row in read_csv('downloads/rows/sxx4-xhzg.csv') if row['Latitude']]
def random_lnglat():
    print 'selecting a random coordinate'
    return sample(sxx4_xhzg, 1)[0]

def main():
    try:
        os.mkdir(GEOJSON_DIR)
    except OSError:
        pass

    views = filter(lambda view: '.json' == view[-5:], os.listdir(VIEWS_DIR))
    for view in views:
        f = open(os.path.join(VIEWS_DIR, view))
        data = json.load(f)
        f.close()
        address_columns = address(data['columns'])
        description_columns = description(data['columns'])

        viewid = view.split('.')[0]
        corresponding_csv = os.path.join(ROWS_DIR, viewid + '.csv')
        corresponding_geojson = os.path.join(GEOJSON_DIR, viewid + '.json')

        # Skip files that are done.
        if os.path.exists(corresponding_geojson):
            continue

        # Skip files without addresses.
        elif address_columns == (None, None):
            continue

        # Skip files without corresponding csv files
        # (I didn't download the largest ones.)
        elif not os.path.exists(corresponding_csv):
            continue

        print 'Creating geoJSON for %s' % view

        data_out = list(geojson(viewid, address_columns, description_columns))
        if data_out != []:
            f = open(os.path.join(GEOJSON_DIR, viewid + '.json'), 'w')
            json.dump(data_out, f)
            f.close

def find_latlng_column(row):
    "Find the coordinates if they're already in there."
    for k, v in row.items():
        if len(re.findall(LATLNG, v)) > 0:
            return k
    return None

def get_lnglat(latlng_cell):
    'Get the coordinates out of a cell.'
    return tuple(reversed(map(float, re.findall(LATLNG, latlng_cell)[0])))

def annoying_get(row, column_name):
    'Try simplifying the column names to deal with encoding.'
    for k,v in row.items():
        if re.sub(ANNOYING, '', k) == re.sub(ANNOYING, '', column_name):
            return v


def geojson(viewid, address_columns, description_columns):
    csv = read_csv(os.path.join(ROWS_DIR, viewid + '.csv'))

    for row in csv:

        latlng_column = find_latlng_column(row)
        street_column, zipcode_column = address_columns

        if latlng_column:
            coords = get_lnglat(row[latlng_column])
        elif not street_column and annoying_get(row, zipcode_column):
            address = 'New York, NY, %s' % annoying_get(row, zipcode_column)
            coords = geocode(address)
        elif not zipcode_column and annoying_get(row, street_column):
            address = '%s, New York, NY' % annoying_get(row, street_column)
            coords = geocode(address)
        elif annoying_get(row, street_column) and annoying_get(row, zipcode_column):
            street  = annoying_get(row, street_column)
            zipcode = annoying_get(row, zipcode_column)
            if zipcode in street:
                address = '%s, New York, NY' % street
            else:
                address = '%s, New York, NY, %s' % (street, zipcode)

            coords = geocode(address)
        else:
            coords = random_lnglat()

        description = ',\n'.join(filter(None, [row.get(a, '') for a in description_columns]))

        # Skip addresses that could not be geocoded.
        if coords:
            lng, lat = coords
            yield {
                "type": "Feature",
                "properties": {
                    "popupContent": description,
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [lng, lat],
                }
            }

def column_names(columns):
    'Column names'
    return [column['name'] for column in columns]

def address(columns):
    'Get the address as a list of columns for geocoding.'
    streets = filter(lambda c: 'street' in c.lower() or 'address' in c.lower(), column_names(columns))
    zipcodes= filter(lambda c: 'zip' in c.lower(), column_names(columns))

    if len(streets) > 0:
        these = (streets[:1], zipcodes[:1])
    else:
        these = ([], [])

    return tuple([None if x == [] else x[0] for x in these])

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
    if address == '':
        return None

    url = GEOCODE_URL % urlencode({'q': address})
    handle = get(url, cachedir = 'downloads')
    d = json.load(handle)
    if len(d) > 0:
        return d[0]['lon'], d[0]['lat']
    else:
        return None

if __name__ == '__main__':
    main()

