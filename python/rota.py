#!/usr/bin/python3
# requirements: pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

from __future__ import print_function

from datetime import datetime
from datetime import timedelta
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '1e0BmwuWKUBP3GWwcdWEtUyNRjqlFzLVZTVtG5si1pvo'
SHEET_NAME = 'Rota'

FROM = 'info@corshambaptists.org'
TO = 'tims@corshambaptists.org'
bcc_you = 'data@corshambaptists.org'

# the first week in the spreadsheet (must always be a Sunday)
sun1 = datetime(2021,1,3)

def calcSunday():
  now = datetime.now()
  sun2 = (now + timedelta(weeks=1) - timedelta(days=now.isoweekday()))

  print(sun2)
  return sun2

def calcWeek(sun2):
  # No. of weeks passed (1 non-data column hence add 1 to start on B)
  weeks = ((sun2 - sun1).days / 7) + 1
  print(int(weeks))
  return int(weeks)

def calcCol(weeks):
  # work out which column we want
  CHAR1 = " ABCDEFGHIJKLMNOPQRSTUVWXY"
  CHAR2 = "ABCDEFGHIJKLMNOPQRSTUVWXY"
  col = None
  if (weeks <= 24):
    print('single char col')
    col = CHAR2[int(weeks % 26):int(weeks % 26)+1]
  else:
    print('double char col')
    col = CHAR1[int(weeks / 26):int(weeks / 26)+1] + CHAR2[int(weeks % 26):int(weeks % 26)+1]
  print(col)
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
    result = sheet.values().get(spreadsheetId=spreadsheet,
                                range=sheetName+'!A1:'+col+'26').execute()
    values = result.get('values', [])

    html = "<html><body><strong>LEADERS COPY, PLEASE EDIT AS NEEDED AND BCC TO CONGREGATION</strong><p>Hi everyone,</p><p>Here's the plan for this Sunday. If you have any issues please try to arrange a swap."

    if not values:
        print('No data found.')
    else:
        html += '<ul>'
        for row in values:
            if row[weeks] != '-':
                html += ('<li><strong>%s:</strong> %s</li>\n' % (row[0], row[weeks]))
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

    print(html)
    return html

def sendMail(html):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Plan for Sunday Service on " + sun2.strftime("%d %b")
    print(msg['Subject'])
    msg['From'] = FROM
    msg['To'] = TO
    msg['Bcc'] = bcc_you
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
    sun2 = calcSunday()
    weeks = calcWeek(sun2)
    col = calcCol(weeks)
    html = composeMessage(SPREADSHEET_ID, SHEET_NAME, weeks, col)
    try:
        sendMail(html)
    except:
        print('Unable to send message')
