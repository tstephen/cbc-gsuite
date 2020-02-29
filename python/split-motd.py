#!/usr/bin/python3
#
# Split a file into individual message of the day
#
# Assumed input is a plain text file with a title line and each message on a separate
# line including citation and a leading index number.
#
# For example:
# QUOTATIONS FOR CBC BLOG / SOCIAL MEDIA etc MARCH 2020.
#
#
#    1. LOVE IS being willing to have your life complicated by the needs and struggles of others without impatience or anger. (Paul Tripp, Weekly Devotional) 
#
#    2. etc...
#
# Author: Tim Stephenson
# Date:   29 Feb 2020
#

import sys

splitLen = 1          # separators per output file
# if no explicit output name use output.1.txt, output.2.txt, etc.
outputBase = sys.argv[1] if len(sys.argv) == 2 else 'output.'
separator = '\n\n'    # assumes text has blank line between items

# This is shorthand and not friendly with memory
# on very large files, but it works.
input = open('input.txt', 'r').read().split(separator)

at = 1 # skip title line
for lines in range(1, len(input), splitLen):
    # First, get list slice, convert to string and strip whitespace
    outputData = ''.join(input[lines:lines+splitLen]).strip()

    if len(outputData) > 0: # if there's anything left, i.e. not empty line
        # Now open the output file using zfill to ensure always same length...
        output = open(outputBase + str(at).zfill(2) + '.html', 'w')
        # ... manipulate, format and write text ...
        if outputData[0:1].isdigit():
            outputData = outputData[outputData.find('.')+1:]
        attributionStart = outputData.rfind('.')+1
        output.write('<blockquote><p>{0}</p><footer><em>&mdash;{1}</em></footer></blockquote>'
            .format(outputData[:attributionStart].strip(),
                    outputData[attributionStart:].strip()))
        # ... and close the file.
        output.close()

        # Increment the counter
        at += 1
