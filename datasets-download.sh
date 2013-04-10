#!/bin/sh
set -e

download_page() {
  [ -z "$1" ] && echo 'You must specify a page number' && return 1
  wget -O "downloads/datasets/$1.html" "https://data.cityofnewyork.us/browse?limitTo=datasets&page=$1&sortBy=oldest&view_type=table"
}

mkdir -p downloads/datasets
for page in $(seq 1 80); do
  download_page $page
done
