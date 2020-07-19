#!/bin/sh
#wait-for-scraper

set -e
  
FILE='/home/data/graph_data.csv'

until test -f "$FILE"; do
      >&2 echo "no data currently available, waiting on scraper"
        sleep 20
    done
      
>&2 echo "Data available, launching website"
exec $@
