#!/usr/bin/env python2
import os
import json

DIR = os.path.join('downloads', 'views')

def main():
    views = filter(lambda view: '.json' == view[-5:], os.listdir(DIR))
    for view in views:
        f = open(os.path.join(DIR, view))
        data = json.load(f)
        f.close()
        print list(address(data['columns']))

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

def description(columns):
    'Get a description as a list of columns for the pop-up box.'
    filter(lambda c: not ( 'street' in c.lower() or 'address' in c.lower() or 'zip' in c.lower()), column_names(columns))

if __name__ == '__main__':
    main()

