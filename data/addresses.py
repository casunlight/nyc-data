#!/usr/bin/env python2
import os
import json
from urllib import urlencode
from cache import get
from read_csv import read_csv

VIEWS_DIR   = os.path.join('downloads', 'views')
ROWS_DIR    = os.path.join('downloads', 'rows')
GEOJSON_DIR = os.path.join('downloads', 'geojson')

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
        if address_columns == (None, None):
            continue
        elif not os.path.exists(os.path.join(ROWS_DIR, viewid + '.csv')):
            continue

        data_out = list(geojson(viewid, address_columns, description_columns))
        if data_out != []:
            f = open(os.path.join(GEOJSON_DIR, viewid + '.json'), 'w')
            json.dump(data_out, f)
            f.close

def geojson(viewid, address_columns, description_columns):
    csv = read_csv(os.path.join(ROWS_DIR, viewid + '.csv'))

    for row in csv:

        street_column, zipcode_column = address_columns
        if not street_column and zipcode_column in row:
            address = 'New York, NY, %s' % row[zipcode_column]
        elif not zipcode_column and street_column in row:
            address = '%s, New York, NY' % row[street_column]
        elif street_column in row and zipcode_column in row:
            address = '%s, New York, NY, %s' % (row[street_column], row[zipcode_column])
        else:
            raise NotImplementedError('Select a random point.')

        description = ',\n'.join(filter(None, [row.get(a, '') for a in description_columns]))

        # Skip addresses that could not be geocoded.
        coords = geocode(address)
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

