#!/bin/bash
# Copyright 2021-2025 Tim Stephenson
# License: Apache 2.0

if [ -z "${WP_USR_PWD}" ]; then
  echo "Oops! Looks like you did not set WordPress credentials in $WP_USR_PWD, check README.md"
  exit 1
fi

curl -u "$WP_USR_PWD" -v \
  'https://corshambaptists.org/wp-json/wp/v2/wpfc_sermon' \
  -H "Accept: application/json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'date='$YEAR'-'$MONTH'-'$DATE'T10:00:00' \
  -d "slug=$SLUG" \
  -d "status=pending" \
  -d "title=$TITLE" \
  -d "content=Welcome to Corsham Baptist Church. $PREACHER_STR brings the word of God from $PASSAGE. This sermon was preached on Sunday $DATE $MONTH_STR $YEAR at CBC $SVC. We would love to hear from you: https://corshambaptists.org/contact-us/.  We are holders of CCLI streaming licence no%3A 48626." \
  -d "excerpt=$PREACHER_STR brings the word of God from $PASSAGE. This sermon was preached on Sunday $DATE $MONTH_STR $YEAR at CBC $SVC." \
  -d "comment_status=closed" \
  -d "ping_status=open" \
  -d 'sermon_date='$YEAR'-'$MONTH'-'$DATE'T10:00:00' \
  -d "sermon_video_link=$YT_URL" \
  -d "wpfc_preacher=$PREACHER" \
  -d "wpfc_sermon_series=$SERIES" \
  -d "wpfc_bible_book=$BIBLE_BOOK" \
  -d "bible_passage=$PASSAGE" \
  -d "wpfc_service_type=$SERVICE_TYPE" \
| jq .id > sermon_id

