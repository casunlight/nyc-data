AppGen Resources
====

## References
APIs

* http://www.ykombinator.com/
* http://www.namemesh.com/
  * This plus csrf token plus cookie should do it: `http POST http://www.namemesh.com/company-name-generator/ word1=domestic,violence,nyc,health word2=cyclist,bridge,monthly fun=8`

Other tools

* http://stackoverflow.com/questions/8626829/possible-to-create-random-numbers-in-sass-compass

Big Apps information

* http://www.nycedc.com/services/nyc-bigapps/past-competitions
* http://nycbigapps.com/prizes
* http://nycbigapps.com/rules

## Socrata SODA API
Get the schema and metadata of a dataset (with httpie).

    http --json https://data.cityofnewyork.us/views/f4yq-wry5

More about the API

    http://dev.socrata.com/docs/endpoints

We can probably use the API directly in our apps.

## Using
Download the listings from Socrata.

    ./datasets-download.sh

Extract the viewids from them.

    ./datasets-parse.py

Download the metadata for each view.

    ./views-download.sh

## Things to randomize

* Tile server
* Url file extension (php, asp, cgi)
* Font size of title
* App name (from a startup name generator)
* App text (from the TED talk generator)
* App logo (from a logo generator)
* Typeface
* Background texture
* Colors
* Footer stickiness

## Useful queries
Longitude and latitude

    select distinct dataset from (select * from c where column like 'Longitude%' or column like 'Latitude%');

Things with addresses

    cd data/downloads/rows
    head -n1 *|grep -i -B1 zip

## Something
Something gets the address and description from the metadata, then geocodes the addresses
from the rows, caching the geocoder results, and returns a GeoJSON of the table, with the
description concatenated in an appropriate place.

## Things to extract for the map

* Longitude, latitude
* Description (JSON list of all the strings? Biggest cells?)
* Title
* Contact information (Phone number? Website?)
