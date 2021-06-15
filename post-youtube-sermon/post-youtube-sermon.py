#!/usr/bin/python3
#
# Download sermon, extract audio and post to WordPress
#
# Author: Tim Stephenson
# Date:   27 Dec 2020
#

import argparse
import subprocess
import string
import sys

# parse args
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="YouTube url for sermon")
args = parser.parse_args()

# -x = extract audio post download but can also optimise by avoiding video
# download altogether
command = "youtube-dl -x" + args.input
 
res = subprocess.call(command, shell = True)
#the method returns the exit code
 
print("Returned Value: ", res)
