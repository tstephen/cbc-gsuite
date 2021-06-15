#!/usr/bin/python3
#
# Extract audio metadata from m4a file
#
# Author: Tim Stephenson
# Date:   04 Jan 2021
#

import glob  
from mutagen.mp4 import MP4
import numpy as np  

filez = glob.glob("2020_12_27_AM.m4a")
mp4file = MP4(filez[0])   
for tag in mp4file.tags:
    print('{}: {}'.format(tag, mp4file.tags[tag]))
