#!/bin/bash

curl -u $WP_USR_PWD -X 'POST' \
  'https://corshambaptists.org/wp-json/wp/v2/wpfc_sermon' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'date='$YEAR'-'$MONTH'-'$DATE'T10:00:00' \
  -d 'slug='$TITLE \
  -d 'status=pending' \
  -d 'title=The%20good%20news%20by%20Mark%20-%20Sunday%20Service%20('$DATE'%20'$MONTH_STR'%20'$YEAR')' \
  -d 'sermon_description=Welcome%20to%20Corsham%20Baptist%20Church%20service%20for%20Sunday%20Service.%20%20Here%20is%20our%20website%2C%20we%20would%20love%20to%20hear%20from%20you%3A%20https%3A%2F%2Fcorshambaptists.org%2Fcontact-us%2F%E2%80%8B%E2%80%8B%20%20We%20are%20holders%20of%20CCLI%20streaming%20licence%20no%3A%2048626.' \
  -d 'comment_status=closed' \
  -d 'ping_status=open' \
  -d 'sermon_date='$YEAR'-'$MONTH'-'$DATE'T10:00:00' \
  -d 'sermon_video_link='$YT_URL \
  -d 'wpfc_preacher='$PREACHER \
  -d 'wpfc_sermon_series='$SERIES \
  -d 'wpfc_bible_book='$BIBLE_BOOK \
  -d 'bible_passage='$PASSAGE \
  -d 'wpfc_service_type='$SERVICE_TYPE
