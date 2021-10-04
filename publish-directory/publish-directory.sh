###############################################################################
# Copyright 2017-2021 Tim Stephenson and contributors
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not
#  use this file except in compliance with the License.  You may obtain a copy
#  of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations under
#  the License.
#
# Orchestrate a set of individual tasks to publish the latest directory
#
###############################################################################

export DIR=$(dirname $0)
cd $DIR

# kp is python client to knowprocess.com
kp https://api.knowprocess.com/cbc/contacts/?returnFull=true > cbc-directory.json

# see python script in this repo
# requires python3 and Jinja 2.10; pip3 install --upgrade Jinja2
jsonprint -i cbc-directory.json -o cbc-directory.html -t directory.html.j2 

# WebKit command line; sudo apt-get wkhtmltopdf on Ubuntu
# & use local wrapper with virtual x server; sudo apt-get install xvfb
./wkhtmltopdf-headless cbc-directory.html cbc-directory.pdf

# wrapper on pdfjam specifically for creating booklets
# sudo apt-get install texlive-extra-utils
pdfbook2 cbc-directory.pdf

# file is already uploaded manually thru WP interface so just drop replacement file in
sshpass -f /home/tstephen/.ssh/corshamb.txt scp -rP 722 cbc-directory.pdf cbc-directory-book.pdf corshamb@aphrodite.krystal.co.uk:public_html/wp-content/uploads/2019/02/

