#!/usr/bin/python3
#
# Create a test stream and a public one for an uncoming service
# Install requirements: pip3 install -r requirements.txt
#
# Author: Tim Stephenson
#

from __future__ import print_function

import argparse
from datetime import datetime
from datetime import timedelta
import os
import os.path
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from googleapiclient.discovery import build
import googleapiclient.discovery
import googleapiclient.errors

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import requests
from requests.auth import HTTPBasicAuth

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
API_SERVICE_NAME = "youtube"
API_VSN = "v3"

args = None

def create_stream():
    """
    Create a new live stream
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token-yt.json'):
        creds = Credentials.from_authorized_user_file('token-yt.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token-yt.json', 'w') as token:
            token.write(creds.to_json())

    service = build(API_SERVICE_NAME, API_VSN, credentials=creds)

    # Call the YouTube API

    request = service.liveBroadcasts().insert(
        part="snippet,contentDetails,status",
        body={
          "contentDetails": {
            "enableClosedCaptions": True,
            "enableContentEncryption": True,
            "enableDvr": True,
            "enableEmbed": True,
            "recordFromStart": True,
            "startWithSlate": True
          },
          "snippet": {
            "title": "Test broadcast",
            "scheduledStartTime": "2022-04-17T09:15:00",
            "description": "Our Sunday service..."
          },
          "status": {
            "privacyStatus": "unlisted"
          }
        }
    )
    response = request.execute()

    print(response)


def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
    action="store_true")
  return parser.parse_args()

if __name__ == '__main__':
    args = parseArgs()
    plan = create_stream()
