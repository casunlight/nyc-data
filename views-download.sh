#!/bin/sh
set -e

mkdir -p downloads/views
for viewid in $(./datasets-parse.py); do
  test -e "downloads/views/${viewid}.json" || wget -O "downloads/views/${viewid}.json" "https://data.cityofnewyork.us/views/${viewid}.json"
done
