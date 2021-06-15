#!/usr/bin/python3
# 
# Read rota sheet and email to admin for further editing
# Install requirements: pip3 install -r requirements.txt

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
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '1e0BmwuWKUBP3GWwcdWEtUyNRjqlFzLVZTVtG5si1pvo'
SHEET_NAME = 'Rota'
NO_HDR_COLS = 1

FROM = 'info@corshambaptists.org'
TO = 'office@corshambaptists.org'
CC = 'info@corshambaptists.org'
# the first week in the spreadsheet (must always be a Sunday)
SUN1 = datetime(2021,1,3)

args = None

def calcSunday():
  now = datetime.now()
  sun2 = (now + timedelta(weeks=1) - timedelta(days=now.isoweekday()))

  if args.verbose:
    print('  next Sunday is: {} ...'.format(sun2))
  return sun2

def calcWeek(sun2):
  # No. of weeks passed (1 column header means add 1 to start on B etc)
  weeks = ((sun2 - SUN1).days / 7) + NO_HDR_COLS
  if args.verbose:
    print('  column offset is: {} ...'.format(int(weeks)))
  return int(weeks)

def calcCol(weeks):
  # work out which column we want
  CHAR1 = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  CHAR2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  col = None
  if (weeks <= (26-NO_HDR_COLS)):
    col = CHAR2[int(weeks % 26):int(weeks % 26)+1]
    if args.verbose:
      print('  single char col')
  else:
    col = CHAR1[int(weeks / 26):int(weeks / 26)+1] + CHAR2[int(weeks % 26):int(weeks % 26)+1]
    if args.verbose:
      print('  double char col')
  if args.verbose:
    print("  this week's col is: '{}'".format(col))
  return col

def composeMessage(spreadsheet, sheetName, weeks, col):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    range = sheetName+'!A1:'+col+'26'
    if args.verbose:
      print("  reading sheet range: '{}'".format(range))
    result = sheet.values().get(spreadsheetId=spreadsheet,
                                range=range).execute()
    values = result.get('values', [])

    html = "<html><body><strong>DRAFT, PLEASE EDIT AS NEEDED AND FORWARD AS APPROPRIATE</strong><p>Hi everyone,</p><p>Here's the plan for this Sunday. If you have any issues please try to arrange a swap."

    if not values:
        print('No data found.')
    else:
        html += '<ul>'
        for idx, row in enumerate(values):
            if args.verbose:
              print("  processing row {}...".format(idx))
            try:
              if args.verbose:
                print("  ... col {} contains: '{}'".format(weeks, row[weeks]))
              if row[weeks] != None and row[weeks] != '-':
                html += ('<li><strong>%s:</strong> %s</li>\n' % (row[0], row[weeks]))
            except:
              if args.verbose:
                print('  no data in row {} and col {}'.format(idx, weeks))
        html += '</ul>'

        #html += "<p><em>Looking ahead to next week, "
        #        for i, row := range resp2.Values {
        #                if i == 1 {
        #                        //log.Printf("  rows found: %d", len(row));
        #                        fmt.Printf("%s will be leading worship ", row[len(row)-1])
        #                }
        #                if i == 14 {
        #                        fmt.Printf("and %s preaching.</em></p>\n", row[len(row)-1])
        #                }
        #        }
        #}

        html += "<p>Thanks as always for your service to our congregation.</p>"
        html += "<p>The master list is: <a href='https://docs.google.com/spreadsheets/d/%s/'>here.</a></p>\n" % spreadsheet
        html += "<p>All the best,</body></html>"

    print('Message:\n{}'.format(html))
    return html

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
      action="store_true")
  return parser.parse_args()

def sendMail(subject, html):
    msg = MIMEMultipart('alternative')
    msg['From'] = FROM
    msg['To'] = TO
    msg['Cc'] = CC
    msg['Subject'] = subject
    text_part = MIMEText("Please view in an HTML capable mail reader", 'plain')
    html_part = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(text_part)
    msg.attach(html_part)

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.sendmail(FROM, TO, msg.as_string())
    s.quit()

if __name__ == '__main__':
    args = parseArgs()
    sun2 = calcSunday()
    weeks = calcWeek(sun2)
    col = calcCol(weeks)
    subject = "Plan for Sunday Service on " + sun2.strftime("%d %b")
    print('Subject: {}'.format(subject))
    html = composeMessage(SPREADSHEET_ID, SHEET_NAME, weeks, col)
    try:
      sendMail(subject, html)
    except:
      if args.verbose:
        print('Unable to send message, is there a local mail transport agent?')
      sys.exit(-1)
