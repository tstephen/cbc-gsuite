
## Authenticate

https://accounts.google.com/o/oauth2/auth?
  client_id=1084945748469-eg34imk572gdhu83gj5p0an9fut6urp5.apps.googleusercontent.com&
  redirect_uri=http%3A%2F%2Flocalhost%2Foauth2callback&
  scope=https://www.googleapis.com/auth/youtube&
  response_type=code&
  access_type=offline

https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=1020433707922-h4gu5fbe7i4hg4rlcmm6dk5n59ug7597.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%2Foauth2callback&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.force-ssl&access_type=offline


https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=1020433707922-3hno8dmetcud8ptcer8mq8oa16f5qdf3.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%2Foauth2callback&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.force-ssl&access_type=offline


## List first page of live streams

```
curl \
  'https://youtube.googleapis.com/youtube/v3/liveBroadcasts?broadcastStatus=completed&broadcastType=broadcastTypeFilterUnspecified&maxResults=5&key=[YOUR_API_KEY]' \
  --header 'Authorization: Bearer [YOUR_ACCESS_TOKEN]' \
  --header 'Accept: application/json' \
  --compressed
```

## Insert broadcast

Open API explorer
```
https://developers.google.com/youtube/v3/live/docs/liveBroadcasts/insert?hl=en&authuser=2&apix=true&apix_params=%7B%22part%22%3A%5B%22snippet%2CcontentDetails%2Cstatus%22%5D%2C%22resource%22%3A%7B%22snippet%22%3A%7B%22title%22%3A%22Test%20broadcast%22%2C%22scheduledStartTime%22%3A%222022-10-19T09%3A15%3A00%22%2C%22scheduledEndTime%22%3A%222022-10-19T10%3A40%3A00%22%2C%22channelId%22%3A%22UC5tpyZ_6K_hTov2tesd9yTA%22%7D%2C%22contentDetails%22%3A%7B%22enableClosedCaptions%22%3Atrue%2C%22enableContentEncryption%22%3Atrue%2C%22enableDvr%22%3Atrue%2C%22enableEmbed%22%3Atrue%2C%22recordFromStart%22%3Atrue%2C%22startWithSlate%22%3Atrue%7D%2C%22status%22%3A%7B%22privacyStatus%22%3A%22unlisted%22%7D%7D%7D
```

curl: 


