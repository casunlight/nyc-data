#!/bin/sh

mkdir -p downloads/views
for viewid in $(./datasets-parse.py); do
  wget -O "downloads/views/${viewid}.json" "https://data.cityofnewyork.us/views/${viewid}"
done
