#!/bin/bash
#
# Copyright 2021-2022 Tim Stephenson
# License: Apache 2.0

REPORT_ERROR_TO=tim@knowprocess.com
# read WordPress credentials
export WP_USR_PWD=`cat wp-creds`

# get data about the most recent sermon published
META=`curl -u $WP_USR_PWD https://corshambaptists.org/wp-json/wp/v2/wpfc_sermon/ | jq  '{ id: .[0].id, slug: .[0].slug, video_url: .[0].sermon_video_url, sermon_date: .[0].sermon_date }'`
SERMON_ID=`echo $META | jq --raw-output .id`
SERMON_DATE=`echo $META | jq --raw-output .sermon_date`
TITLE=`echo $META | jq --raw-output .slug`

# Allow override of YT_URL as often missing from WP
if [ -z "$YT_URL" ]
then
    YT_URL=`echo $META | jq --raw-output .video_url`
fi
if [ -z "$YT_URL" ]
then
    # No YouTube URL, report error and quit.
    echo "Subject: Unable to post sermon audio" > post-sermon-failure.txt
    echo "Hi, I'm afraid I have been unable to post audio for "$sermon_id" because no YouTube url is specified in WordPress." >> post-sermon-failure.txt
    echo "If this is because there was no stream this week then please ignore this message. However if there was a stream please add the URL and ask me to try again." >> post-sermon-failure.txt
    echo "The CBC bot" >> post-sermon-failure.txt
    cat post-sermon-failure.txt
    sendmail $REPORT_ERROR_TO < post-sermon-failure.txt
    exit -1
fi
# So far, so good, continuing...

SERMON_DATE=`date -d @$SERMON_DATE +"%Y-%m-%d"`
YEAR=${SERMON_DATE:0:4}
MONTH=${SERMON_DATE:5:2}
DATE=${SERMON_DATE:8:2}
NORMAL_TITLE=$YEAR'_'$MONTH'_'$DATE'_'$TITLE

# get the audio component of the live stream
youtube-dl -x --add-metadata -o $TITLE'.%(ext)s' $YT_URL
# avoid file name clash between normalised title and received
if [[ $TITLE == $YEAR-$MONTH-$DATE* ]]; then
    mv $TITLE.m4a tmp-$TITLE.m4a
    TITLE=tmp-$TITLE
fi

# -af: trim silence from start (typically run a pre-live screen for a couple of minutes)
# -ac 1: convert to single channel (mono) since both channels recorded are identical
ffmpeg -i $TITLE.m4a -ac -af silenceremove=stop_periods=-1:stop_duration=1:stop_threshold=-70dB $NORMAL_TITLE.m4a

# push the audio to the web server
echo '  deploying '$NORMAL_TITLE' to '$YEAR'/'$MONTH
## NOTE: this will fail if dir not pre-created
scp -P 722 $NORMAL_TITLE.m4a corshamb@aphrodite.krystal.co.uk:public_html/wp-content/uploads/sermons/$YEAR/$MONTH/

# create a media post for the audio
# this works but it skips the sermons folder from the path so we end up with
# a media record pointing at non-existent file
# However the good news is that we don't need a media record
#curl -u $WP_USR_PWD -H 'Content-Disposition: attachment; filename="'$TITLE.m4a'"' \
#  -d 'jetpack_sharing_enabled=false' \
#  -d 'status=draft' \
#  -X POST \
#  https://corshambaptists.org/wp-json/wp/v2/media/

# link the audio to the sermon post
curl -u $WP_USR_PWD -X 'POST' \
  'https://corshambaptists.org/wp-json/wp/v2/wpfc_sermon/'$SERMON_ID \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'sermon_date='`date --date=$SERMON_DATE +%s` \
  -d 'sermon_audio=https%3A%2F%2Fcorshambaptists.org%2Fwp-content%2Fuploads%2Fsermons%2F'$YEAR'%2F'$MONTH'%2F'$NORMAL_TITLE'.m4a'

