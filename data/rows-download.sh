#!/bin/sh
set -e

mkdir -p downloads/rows
for viewid in $(./datasets-parse.py); do
  grep 311\ Service\ Requests "downloads/views/${viewid}.json" && continue
  test -e "downloads/rows/${viewid}.csv" || curl "https://data.cityofnewyork.us/api/views/${viewid}/rows.csv?accessType=DOWNLOAD" > "downloads/rows/${viewid}.csv"
done
