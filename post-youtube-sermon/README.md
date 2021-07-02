
##  Steps involved

1. Post a bare bones sermon entry with date, preacher etc.
1. (After the service) Get the audio and meta-data from the already published YouTube video ;
2. Post the audio to WordPress media library
3. Get the transcript (manually written and shared)
4. Update the existing sermon entry in WordPress with audio and transcript (maybe doing each separately as not sure when each will arrive)

## Fetch audio and metadata from YouTube

(youtube-dl)[https://github.com/ytdl-org/youtube-dl] is a cross-platform, command-line tool for fetching all manner of data from YouTube and other sharing sites. This will fetch audio only and add meta-data such as the YouTube description and so forth as audio tags.

```
youtube-dl --add-metadata -x https://youtu.be/id
```

## Authentication

It's worth knowing that the REST API is designed first and foremost for use within the web server so to use it remotely requires an alternative authentication mechanism. I'm using Application Passwords.

## Create sermon via the command line

First you need to know the `post_type` of sermons. You can list those available to the REST API with:

```
curl -u "username:application password"  https://corshambaptists.org/wp-json/wp/v2/types | jq
```

Note that it seems possible to have custom post types that are not exposed over REST API. Check this stack overflow for how to resolve that: https://wordpress.stackexchange.com/questions/294085/wordpress-rest-create-post-of-custom-type

The Sermon Manager for WordPress uses the type `wpfc_sermon` and here's an example of setting the necessary fields

```
curl -u "username:application password" -X POST -d "title=New Title" https://corshambaptists.org/wp-json/wp/v2/wpfc_sermon
```

```
export PUB_DATE=2020-12-27
export PREACHER=69
export SERVICE_TYPE=494
curl -u "tims@corshambaptists.org:h39d Fbx0 FqVA tBbr Fs4b nhKY" -X POST -d 'date='$PUB_DATE'T10:00:00' -d 'slug='$PUB_DATE -d 'status=pending' \
  -d 'wpfc_preacher='$PREACHER, \
  -d 'wpfc_sermon_series='$SERIES, \
  -d 'wpfc_sermon_topics=', \
  -d 'wpfc_bible_book='$BIBLE_BOOKS, \
  -d 'wpfc_service_type='$SERVICE_TYPE, \
  -d 'sermon_audio=https://corshambaptists.org/wp-content/uploads/sermons/2020/12/20201213.Matthew2_1-12.Advent3.audio_.mp3', \
  -d 'bible_passage=Matthew 2:1-12', \
  -d 'sermon_description=<p>In our third advent sermon at church on the green, we look at Herod and ask why God allowed him to act as he did.</p>', \
  -d 'sermon_video_url=https://youtu.be/Wky1qbvoFCI', \
  -d 'sermon_bulletin=' \
  -d 'sermon_date='$PUB_DATE \
  -d '_featured_url=https://corshambaptists.org/wp-content/uploads/sermons/2020/12/VideoCover_Sermon_Advent3.png' -d 'title=Loving Kindness - Sunday Service (27 Dec 2020)' https://corshambaptists.org/wp-json/wp/v2/wpfc_sermon
```

  -d 'featured_media=11061', \
  -d 'comment_status=closed', \
  -d 'ping_status=open', \
  -d 'jetpack_sharing_enabled=true', \
  -d 'jetpack_likes_enabled=true', \

## Check the result in all its detail
```
curl -u "username:application password" https://corshambaptists.org/wp-json/wp/v2/wpfc_sermon/11064
```
