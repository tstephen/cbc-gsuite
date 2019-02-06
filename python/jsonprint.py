#!/usr/bin/python3
###############################################################################
# Copyright 2015-2018 Tim Stephenson and contributors
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
# Render JSON using Jinja template
#
# - Install Jinja: pip install Jinja2
# - Reference: http://jinja.pocoo.org/
#
###############################################################################
import argparse
from jinja2 import Template
import json

# parse args
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--json", help="payload")
parser.add_argument("-o", "--output", help="output file")
parser.add_argument("-t", "--template", help="template file")
parser.add_argument("-v", "--verbose", help="increase output verbosity",
    action="store_true")
args = parser.parse_args()

fJson = open(args.json,'r')
sJson = json.load(fJson)                

fTemplate = open(args.template,'r')         
sTemplate = fTemplate.read()                

template = Template(sTemplate)
html = template.render(contacts = sJson)

file = open(args.output,'w') 
file.write(html) 
file.close() 
