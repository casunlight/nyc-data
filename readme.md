AppGen Resources
====

## References
APIs

* http://www.ykombinator.com/
* http://www.namemesh.com/

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
