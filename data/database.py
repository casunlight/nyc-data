#!/usr/bin/env python2
import os
import json
import dumptruck

dt = dumptruck.DumpTruck(dbname = '/tmp/nyc-open-data.db')
DIR = os.path.join('downloads', 'views')

views = filter(lambda view: '.json' == view[-5:], os.listdir(DIR))
for view in views:
    f = open(os.path.join(DIR, view))
    data = json.load(f)
    f.close()
    dt.insert([{'column': column['name'], 'dataset': data['id']} for column in data['columns']])
