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

def address(columns):
    'Get the address as a list of columns for geocoding.'
    for word in ['street', 'address', 'zip']:
        for column in columns:
            if word in column.lower():
                yield street


def description(columns):
    'Get a description as a list of columns for the pop-up box.'

if __name__ == '__main__':
    main()

