#!/bin/bash

# read WordPress credentials
WP_USR_PWD=`cat wp-creds`

# get data about the most recent sermon published
META=`curl -u $WP_USR_PWD https://corshambaptists.org/wp-json/wp/v2/wpfc_sermon/ | jq  '{ id: .[0].id, slug: .[0].slug, video_url: .[0].sermon_video_url }'`
SERMON_ID=`echo $META | jq --raw-output .id`
TITLE=`echo $META | jq --raw-output .slug`
YT_URL=`echo $META | jq --raw-output .video_url`

# get the audio component of the live stream
youtube-dl -x --add-metadata -o $TITLE'.%(ext)s' $YT_URL

# push the audio to the web server
echo '  deploying '$TITLE' to '$YEAR'/'$MONTH
scp -P 722 $TITLE.m4a corshamb@aphrodite.krystal.co.uk:public_html/wp-content/uploads/sermons/$YEAR/$MONTH/

# create a media post for the audio
curl -u $WP_USR_PWD -H 'Content-Disposition: attachment; filename="'$TITLE.m4a'"' \
  -d 'jetpack_sharing_enabled=false' \
  -d 'status=draft' \
  -X POST \
  https://corshambaptists.org/wp-json/wp/v2/media/

# link the audio to the sermon post
curl -u $WP_USR_PWD -X 'POST' \
  'https://corshambaptists.org/wp-json/wp/v2/wpfc_sermon/'$SERMON_ID \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'sermon_audio=https%3A%2F%2Fcorshambaptists.org%2Fwp-content%2Fuploads%2Fsermons%2F'$YEAR'%2F'$MONTH'%2F'$TITLE'.m4a'

