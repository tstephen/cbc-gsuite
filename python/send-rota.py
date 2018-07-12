#!/usr/bin/python3
from datetime import datetime
from datetime import timedelta
import os
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from_me = 'info@corshambaptists.org'
to_you = 'tim@thestephensons.me.uk'
# the first week in the spreadsheet (will always be a Sunday)
sun1 = datetime(2018,7,15)
# calculate next sunday date
now = datetime.now()
sun2 = (now + timedelta(weeks=1) - timedelta(days=now.isoweekday()))
# No. of weeks passed (2 non-data columns hence add 2 to start on C)
weeks = ((sun2 - sun1).days / 7) + 2
# work out which column we want
CHAR1 = " ABCDEFGHIJKLMNOPQRSTUVWXY"
CHAR2 = "ABCDEFGHIJKLMNOPQRSTUVWXY"
col = None
if (weeks <= 26):
  col = CHAR2[int(weeks % 26):int(weeks % 26)+1]
else:
  col = CHAR1[int(weeks / 26):int(weeks / 26)+1] + CHAR2[int(weeks % 26):int(weeks % 26)+1]
#print(col)

html = os.popen("rota " + col).read()
print(html)

msg = MIMEMultipart('alternative')
msg['Subject'] = "Plan for 9:15 on " + sun2.strftime("%d %b")
print(msg['Subject'])
msg['From'] = from_me 
msg['To'] = to_you
text_part = MIMEText("Please view in an HTML capable mail reader", 'plain')
html_part = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(text_part)
msg.attach(html_part)

# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost')
s.sendmail(from_me, to_you, msg.as_string())
s.quit()
