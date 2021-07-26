
##  Steps involved

1. Post a bare bones sermon entry with date, preacher etc.
2. (After the service) Get the audio and meta-data from the already published YouTube video ;
3. Post the audio to WordPress media library
4. Update the existing sermon entry in WordPress with audio

## Fetch audio and metadata from YouTube

[youtube-dl](https://github.com/ytdl-org/youtube-dl) is a cross-platform, command-line tool for fetching all manner of data from YouTube and other sharing sites. This will fetch audio only(so much smaller) and add meta-data such as the YouTube description and so forth as audio tags.

```
youtube-dl --add-metadata -x https://youtu.be/id
```

## Interacting with WordPress via the API

For some time now, WordPress has had an API, which is obviously more suitable for automation and therefore means there's less work to manage the site. However documentation is a bit sparse. My preferred language for this kind of thing is python because it's simple, interpreted and cross-platform. However, despite the excellent [requests](https://docs.python-requests.org/en/master/index.html) library, I was not able to do some of the calls below so I've left them as `curl commands`. If you find you have to use Windows try installing the [Windows Sub-system for Linux](https://docs.microsoft.com/en-us/windows/wsl/about).

### Environment variables

It's worth noting that the REST API appears to be designed first and foremost for use within the web server so it hasn't (yet) prioritised authentication mechanisms now common for APIs (OAuth). So to slightly reduce the risk exposing my password I pass it into scripts as .n environment variable. A few other things are externalised this way too. Example (non-functional) values are included in `env.sample.sh`.

## Create sermon via the command line

First you need to know the `post_type` of sermons. You can list those available to the REST API with:

```
curl -u $WP_USR_PWD  https://corshambaptists.org/wp-json/wp/v2/types | jq
```

Note that it seems possible to have custom post types that are not exposed over REST API. Check this stack overflow for how to resolve that: https://wordpress.stackexchange.com/questions/294085/wordpress-rest-create-post-of-custom-type

The Sermon Manager for WordPress uses the type `wpfc_sermon` and here's an example of setting the necessary fields. Note that for many fields you need to look up their numeric id rather than using the human readable name, e.g. preacher is here 69 rather than 'Eddie'.

```
curl -u $WP_USR_PWD -X POST \
  -d 'date='$YEAR'-'$MONTH'-'$DATE'T10:00:00' \
  -d 'slug='$TITLE \
  -d 'status=pending' \
  -d 'wpfc_preacher='$PREACHER, \
  -d 'wpfc_sermon_series='$SERIES, \
  -d 'wpfc_sermon_topics=', \
  -d 'wpfc_bible_book='$BIBLE_BOOK, \
  -d 'wpfc_service_type='$SERVICE_TYPE, \
  -d 'sermon_audio=https://corshambaptists.org/wp-content/uploads/sermons/'$YEAR'/'$MONTH'/'$DATE'/'$TITLE.mp3', \
  -d 'bible_passage=Matthew 2:1-12', \
  -d 'sermon_description=<p>In our third advent sermon at church on the green, we look at Herod and ask why God allowed him to act as he did.</p>', \
  -d 'sermon_video_url='$YT_URL, \
  -d 'sermon_bulletin=' \
  -d 'sermon_date='$YEAR'-'$MONTH'-'$DATE'T10:00:00' \
  -d 'title=Loving Kindness - Sunday Service (27 Dec 2020)' \
  https://corshambaptists.org/wp-json/wp/v2/wpfc_sermon
```

This command will return the full sermon record. Note it will start with the id used to check the result below.

Check the result in all its detail:

```
curl -u $WP_USR_PWD https://corshambaptists.org/wp-json/wp/v2/wpfc_sermon/11064
```

## Post audio file

It would appear that the WP API expects the file to be delivered to the server already (for example using `scp`. I placed it in the same location that uploading through the user interface would.

### Create a new media library entry for the sermon audio

You might consider this is not necessary because the sermon will reference the audio simply by url, but if you want to hold the file to appear in the media library, for example to include in any other posts, this will do that.

  ```
  curl -u $WP_USR_PWD -H 'Content-Disposition: attachment; filename="'$TITLE'.mp3"' -d 'status=draft' -X POST https://corshambaptists.org/wp-json/wp/v2/media/
  ```

Again you will receive an id that can be used to check the result:

  ```
  curl -u $WP_USR_PWD https://corshambaptists.org/wp-json/wp/v2/media/12469
  ```

## Link to the audio to the sermon post

Note the id must once again be replaced in the below.

```
curl -u $WP_USR_PWD -X 'POST' \
  'https://corshambaptists.org/wp-json/wp/v2/wpfc_sermon/12659' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'sermon_audio=https%3A%2F%2Fcorshambaptists.org%2Fwp-content%2Fuploads%2Fsermons%2F'$YEAR'%2F'$MONTH'%2F'$TITLE'.m4a'#
```
