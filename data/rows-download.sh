#!/bin/sh
set -e

mkdir -p downloads/rows
for viewid in $(./datasets-parse.py); do
  test -e "downloads/rows/${viewid}.csv" || curl "https://data.cityofnewyork.us/api/views/${viewid}.csv?accessType=DOWNLOAD" > "downloads/rows/${viewid}.csv"
done
