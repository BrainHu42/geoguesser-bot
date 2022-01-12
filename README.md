# GeoGuesser Bot
This bot uses OSM and wikidata APIs to periodically post images of notable locations on Instagram and Twitter and reply to people that guess the name or address correctly. Currently hosted on AWS Lambda.
Follow @name_this_place on Twitter and @guess_this_place on Instagram

# Design Challenges
- Efficiently querying Open Street Map API for a random yet notable location 
- Dealing with gaps in coverage. (i.e. if wikidata doesn't have an image/description for OSM location or vice versa)
