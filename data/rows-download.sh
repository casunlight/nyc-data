#!/bin/sh
set -e

mkdir -p downloads/rows
for viewid in $(./datasets-parse.py); do
  grep 311\ Service\ Requests "downloads/views/${viewid}.json" > /dev/null && continue
  [ 'ym2h-u9dt' = "${viewid}" ] && continue
  [ 's22f-jsd4' = "${viewid}" ] && continue
  test -e "downloads/rows/${viewid}.csv" || curl "https://data.cityofnewyork.us/api/views/${viewid}/rows.csv?accessType=DOWNLOAD" > "downloads/rows/${viewid}.csv"
done
