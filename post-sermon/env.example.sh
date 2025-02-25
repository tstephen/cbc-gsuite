#!/bin/bash

# 1 Samuel = 623
# Mark = 147
# Luke = 152
export BIBLE_BOOK=152
export DATE=`date +%d`
export MONTH=`date +%m`
export MONTH_STR=`date +%b`
export PASSAGE="Luke 8:40-48"
# Adam = 594
export PREACHER=594
export PREACHER_STR='Adam Jacques'
# Luke 2024-25 = 620
export SERIES=620
# Neston = 602
export SERVICE_TYPE=602
export SLUG=$YEAR'-'$MONTH'-'$DATE'-'${PASSAGE// /-}
export SVC='Neston'
# format like: 1 Samuel 23 – Sunday 16th February 2025 – David Morrell
export TITLE=$PASSAGE' - Sunday '$DATE' '$MONTH_STR' '$YEAR' - '$PREACHER_STR
export WP_USR_PWD='username@corshambaptists.org:application password with or without spaces'
export YEAR=`date +%Y`
export YT_URL='https://youtu.be/smkk8OkpX48'
