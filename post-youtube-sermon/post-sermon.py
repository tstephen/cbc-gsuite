#!/usr/bin/python3
#
# Post a new sermon to WordPress
#
# Author: Tim Stephenson
# Date:   30 Dec 2020
#

import argparse
import calendar
import datetime
import subprocess
import string
import sys
import urllib3

# parse args
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--bible", help="Bible passage")
parser.add_argument("-e", "--extract", default="", help="Short description (optional)")
parser.add_argument("-d", "--date", help="Date of sermon (yyyy-mm-dd)")
parser.add_argument("-f", "--featured-image", help="Featured image id")
parser.add_argument("-i", "--input", help="Audio file for sermon")
parser.add_argument("-n", "--notices", default="", help="URL for notices (optional)")
parser.add_argument("-p", "--preacher", default="69", help="Preacher id (defaults to Eddie:69)")
parser.add_argument("-s", "--series", default="231", help="Sermon series (defaults to One-offs)")
parser.add_argument("-u", "--user", help="User:Password")
parser.add_argument("-v", "--video", help="Video url")
args = parser.parse_args()

# non-user defaults
bible_books = []
pub_date = args.date + 'T10:00:00'
sermon_topics = []
service_type = 494
slug = args.date
status = 'future'

comment_status = 'closed'
ping_status = 'open'
jetpack_sharing_enabled = True
jetpack_likes_enabled = True

endpoint = 'https://corshambaptists.org/wp-json/wp/v2/wpfc_sermon'
now = datetime.datetime.now()

# POST request
try:
  http = urllib3.PoolManager()
  r = http.request(
    'POST',
    endpoint,
    headers = urllib3.make_headers(basic_auth=args.user),
    fields = {
      'bible_passage': args.bible,
      'comment_status': comment_status,
      'content': args.extract,
      'date': pub_date,
      'extract': args.extract,
      'ping_status': ping_status,
      'sermon_audio': 'https://corshambaptists.org/wp-content/uploads/sermons/{}/{}/{}'.format(now.year, str(now.month).zfill(2), args.input),
      'sermon_bulletin': args.notices,
      'sermon_date': args.date,
      'sermon_description': args.extract,
      'sermon_video_url': args.video,
      'slug': slug,
      'status': status,
      'title': 'Service for {} {} {}'.format(args.date[8:10], calendar.month_name[int(args.date[5:7])], args.date[0:4]),
      'wpfc_bible_book': ''.join(bible_books),
      'wpfc_preacher': args.preacher,
      'series_wpfc_sermon': args.series,
      'wpfc_sermon_topics': ''.join(sermon_topics),
      'wpfc_service_type': service_type
    }
  )
except urllib3.exceptions.HTTPError as e:
  print('ERROR: {}: {}'.format(e.code, e.reason))
  print('  {}', e)

print('SUCCESS: {}', r.data)
