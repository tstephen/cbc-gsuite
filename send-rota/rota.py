#!/usr/bin/python3
#
# Read rota sheet and email to admin for further editing
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
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import requests
from requests.auth import HTTPBasicAuth

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SHEET_ID = '1e0BmwuWKUBP3GWwcdWEtUyNRjqlFzLVZTVtG5si1pvo'
TAB_NAME = 'Rota'

FROM = 'noreply@knowprocess.com'
TO = 'data@corshambaptists.org'
BCC = 'tim@knowprocess.com'
# the first week in the spreadsheet must be first Sunday of the current year
NYD =  datetime.now().replace(day=1,month=1)
SUN1 = NYD.replace(day=1+(6-NYD.weekday()))

args = None

def calcSunday():
  now = datetime.now()
  sun2 = (now + timedelta(weeks=1) - timedelta(days=now.isoweekday()))

  if args.verbose:
    print('  next Sunday is: {} ...'.format(sun2))
  return sun2

def calcWeek(sun2):
  # No. of weeks passed (1 column header means add 1 to start on B etc)
  weeks = ((sun2 - SUN1).days / 7) + args.headingcolumns
  if args.verbose:
    print('  column offset is: {} ...'.format(int(weeks)))
  return int(weeks)

def calcCol(weeks):
  # work out which column we want
  CHAR1 = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  CHAR2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  col = None
  if (weeks <= (26-args.headingcolumns)):
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

    plan = { 'service':values[0][0] }
    if args.verbose:
      print("  found service '{}'".format(values[0][0]))

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
                plan[row[0]] = row[weeks]
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
    plan['html'] = html
    return plan

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
    action="store_true")
  parser.add_argument("-s", "--sheet", help="specify the source Google sheet",
    default=SHEET_ID)
  parser.add_argument("-t", "--tab", help="specify the source tab",
    default=TAB_NAME)
  parser.add_argument("-hc", "--headingcolumns", help="number of heading columns",
    type=int, default=2)
  parser.add_argument("-cc", "--cc", help="comma-separated list of email addresses to cc",
    default="")
  return parser.parse_args()

def sendMail(subject, html):
    msg = MIMEMultipart('alternative')
    msg['From'] = FROM
    msg['To'] = TO
    msg['Cc'] = args.cc
    recipients = args.cc.split(",") + BCC.split(",") + [TO]
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
    s.sendmail(FROM, recipients, msg.as_string())
    s.quit()

def startProc(plan):
    if args.verbose:
      print('Starting workflow with {} ...'.format(plan))

    json = { "processDefinitionKey": "PlanService", "businessKey": plan['subject'], "variables": [] }

    if 'service' in plan:
      json['variables'].append({ "name": "service", "type": "string", "value": plan['service'] })
    if 'serviceDate' in plan:
      json['variables'].append({ "name": "serviceDate", "type": "string", "value": plan['serviceDate'] })
    if 'Worship leader' in plan:
      json['variables'].append({ "name": "worshipLeader", "type": "string", "value": plan['Worship leader'] })
    if 'Intercessory prayer' in plan:
      json['variables'].append({ "name": "intercessor", "type": "string", "value": plan['Intercessory prayer'] })
    if 'Passage' in plan:
      json['variables'].append({ "name": "passage", "type": "string", "value": plan['Passage'] })
    if 'Preacher' in plan:
      json['variables'].append({ "name": "preacher", "type": "string", "value": plan['Preacher'] })
    if 'Service co-ordination' in plan:
      json['variables'].append({ "name": "serviceCoordinator", "type": "string", "value": plan['Service co-ordination'] })
    if 'Video streaming' in plan:
      json['variables'].append({ "name": "stream", "type": "string", "value": plan['Video streaming'] })
    if 'Sound' in plan:
      json['variables'].append({ "name": "sound", "type": "string", "value": plan['Sound'] })
    if 'html' in plan:
      json['variables'].append({ "name": "message", "type": "string", "value": plan['html'] })

    f = open("flowable-creds", "r")
    flowableCreds = f.read().strip()

    r = requests.post('https://flowable.knowprocess.com/flowable-rest/service/runtime/process-instances',
        auth=('info@corshambaptists.org', flowableCreds),
        json=json)

if __name__ == '__main__':
    args = parseArgs()
    sun2 = calcSunday()
    weeks = calcWeek(sun2)
    col = calcCol(weeks)
    plan = composeMessage(args.sheet, args.tab, weeks, col)
    plan['serviceDate'] = sun2.strftime("%Y-%m-%d")
    plan['subject'] = "Plan for {} Service on {}".format(plan['service'], plan['Date'])
    print('Subject: {}'.format(plan['subject']))
    try:
      sendMail(plan['subject'], plan['html'])
      startProc(plan);
    except Exception as e:
      if args.verbose:
        print('Unable to send message or start workflow; check credentials and local mail transport agent')
        print(e)
      sys.exit(-1)
    else:
      if args.verbose:
        print('Sent message and started workflow successfully')
      sys.exit(0)
