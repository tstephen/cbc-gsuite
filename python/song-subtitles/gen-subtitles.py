#!/usr/bin/python3
#
# Split a file into individual lines and generate SVG to use as subtitles.
#
# Assumed input is a plain text file. Lines starting # will be ignored.
#
# Author: Tim Stephenson
# Date:   08 Dec 2020
#

import argparse
import sys

# parse args
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--color", default="ffdd00", help="foreground colour")
parser.add_argument("-f", "--font", default="Raleway", help="font")
parser.add_argument("-i", "--input", default="input.txt", help="input.txt")
parser.add_argument("-o", "--output", default="output.", help="base output file")
args = parser.parse_args()

template = '''<?xml version="1.0" ?><!-- Created with Inkscape (http://www.inkscape.org/) --><svg xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="1920" height="1080" id="svg2383" sodipodi:version="0.32" inkscape:version="0.92.2 (5c3e80d, 2017-08-06)" version="1.0" sodipodi:docname="Bar_3.svg" inkscape:output_extension="org.inkscape.output.svg.inkscape">
  <defs id="defs2385">
    <linearGradient inkscape:collect="always" id="linearGradient3636">
      <stop style="stop-color:#000000;stop-opacity:0.4" offset="0" id="stop3638"/>
      <stop style="stop-color:#000000;stop-opacity:0.85" offset="1" id="stop3640"/>
    </linearGradient>
    <linearGradient inkscape:collect="always" id="linearGradient3684">
      <stop style="stop-color:#dea436;stop-opacity:1" offset="0" id="stop3686"/>
      <stop style="stop-color:#f8c050;stop-opacity:1" offset="1" id="stop3688"/>
    </linearGradient>
    <linearGradient id="linearGradient3670" inkscape:collect="always">
      <stop id="stop3672" offset="0" style="stop-color:#dcaa38;stop-opacity:1"/>
      <stop id="stop3674" offset="1" style="stop-color:#f4c54f;stop-opacity:1"/>
    </linearGradient>
    <linearGradient inkscape:collect="always" id="linearGradient3182">
      <stop style="stop-color:#ffffff;stop-opacity:0.55" offset="0" id="stop3184"/>
      <stop style="stop-color:#ffffff;stop-opacity:0;" offset="1" id="stop3186"/>
    </linearGradient>
    <linearGradient inkscape:collect="always" id="linearGradient3174">
      <stop style="stop-color:#324da7;stop-opacity:0.55" offset="0" id="stop3176"/>
      <stop style="stop-color:#324da7;stop-opacity:0;" offset="1" id="stop3178"/>
    </linearGradient>
    <linearGradient inkscape:collect="always" id="linearGradient3190">
      <stop style="stop-color:#324da7;stop-opacity:1" offset="0" id="stop3192"/>
      <stop style="stop-color:#324da7;stop-opacity:0;" offset="1" id="stop3194"/>
    </linearGradient>
    <linearGradient inkscape:collect="always" id="linearGradient3267">
      <stop style="stop-color:#0000ff;stop-opacity:0" offset="0" id="stop3269"/>
      <stop id="stop3275" offset="0.48768985" style="stop-color:#ffffff;stop-opacity:1"/>
      <stop style="stop-color:#0000ff;stop-opacity:0;" offset="1" id="stop3271"/>
    </linearGradient>
    <inkscape:perspective sodipodi:type="inkscape:persp3d" inkscape:vp_x="0 : 526.18109 : 1" inkscape:vp_y="0 : 1000 : 0" inkscape:vp_z="744.09448 : 526.18109 : 1" inkscape:persp3d-origin="372.04724 : 350.78739 : 1" id="perspective2391"/>
    <linearGradient inkscape:collect="always" xlink:href="#linearGradient3267" id="linearGradient3273" x1="333.26617" y1="671.26709" x2="1668.8561" y2="671.26709" gradientUnits="userSpaceOnUse" gradientTransform="matrix(0.4475832,0,0,1.1594093,-317.72844,-354.23847)"/>
    <linearGradient inkscape:collect="always" xlink:href="#linearGradient3267" id="linearGradient3463" gradientUnits="userSpaceOnUse" gradientTransform="matrix(0.4475832,0,0,1.1594093,-317.72845,-255.93349)" x1="333.26617" y1="671.26709" x2="1668.8561" y2="671.26709"/>
    <linearGradient inkscape:collect="always" xlink:href="#linearGradient3190" id="linearGradient3196" x1="1917.6716" y1="542.59882" x2="1622.8263" y2="542.59882" gradientUnits="userSpaceOnUse" gradientTransform="translate(-480.00173,0)"/>
    <linearGradient inkscape:collect="always" xlink:href="#linearGradient3190" id="linearGradient3200" gradientUnits="userSpaceOnUse" x1="1917.6716" y1="542.59882" x2="1622.8263" y2="542.59882" gradientTransform="matrix(-1,0,0,1,1920.0025,7.77e-2)"/>
    <linearGradient inkscape:collect="always" xlink:href="#linearGradient3174" id="linearGradient3180" x1="513.01154" y1="-540.84637" x2="513.01154" y2="-636.17462" gradientUnits="userSpaceOnUse"/>
    <linearGradient inkscape:collect="always" xlink:href="#linearGradient3182" id="linearGradient3188" x1="719.99805" y1="-540.84637" x2="719.99805" y2="-631.5105" gradientUnits="userSpaceOnUse"/>
    <linearGradient inkscape:collect="always" xlink:href="#linearGradient3174" id="linearGradient3197" gradientUnits="userSpaceOnUse" x1="513.01154" y1="-540.84637" x2="513.01154" y2="-636.17462"/>
    <linearGradient inkscape:collect="always" xlink:href="#linearGradient3182" id="linearGradient3199" gradientUnits="userSpaceOnUse" x1="719.99805" y1="-540.84637" x2="719.99805" y2="-631.5105"/>
    <linearGradient inkscape:collect="always" xlink:href="#linearGradient3174" id="linearGradient2841" gradientUnits="userSpaceOnUse" x1="513.01154" y1="-540.84637" x2="513.01154" y2="-636.17462" gradientTransform="translate(240.00003,-1.7053223)"/>
    <linearGradient inkscape:collect="always" xlink:href="#linearGradient3182" id="linearGradient2843" gradientUnits="userSpaceOnUse" x1="719.99805" y1="-540.84637" x2="719.99805" y2="-631.5105" gradientTransform="translate(240.00003,-1.7053223)"/>
    <inkscape:perspective id="perspective2855" inkscape:persp3d-origin="0.5 : 0.33333333 : 1" inkscape:vp_z="1 : 0.5 : 1" inkscape:vp_y="0 : 1000 : 0" inkscape:vp_x="0 : 0.5 : 1" sodipodi:type="inkscape:persp3d"/>
    <radialGradient inkscape:collect="always" xlink:href="#linearGradient3670" id="radialGradient3654" cx="922.56451" cy="413.05423" fx="922.56451" fy="413.05423" r="638.25861" gradientTransform="matrix(1,0,0,0.05818239,-200.15323,977.43371)" gradientUnits="userSpaceOnUse"/>
    <inkscape:perspective id="perspective3664" inkscape:persp3d-origin="0.5 : 0.33333333 : 1" inkscape:vp_z="1 : 0.5 : 1" inkscape:vp_y="0 : 1000 : 0" inkscape:vp_x="0 : 0.5 : 1" sodipodi:type="inkscape:persp3d"/>
    <radialGradient inkscape:collect="always" xlink:href="#linearGradient3684" id="radialGradient3682" cx="959.99805" cy="514.13556" fx="959.99805" fy="514.13556" r="781.3515" gradientTransform="matrix(1,0,0,0.04078534,0,493.16635)" gradientUnits="userSpaceOnUse"/>
    <filter id="filter3984" inkscape:label="Drop shadow" width="1.5" height="1.5" x="-.25" y="-.25">
      <feGaussianBlur id="feGaussianBlur3986" in="SourceAlpha" stdDeviation="1.000000" result="blur"/>
      <feColorMatrix id="feColorMatrix3988" result="bluralpha" type="matrix" values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1.000000 0 "/>
      <feOffset id="feOffset3990" in="bluralpha" dx="0.000000" dy="4.000000" result="offsetBlur"/>
      <feMerge id="feMerge3992">
        <feMergeNode id="feMergeNode3994" in="offsetBlur"/>
        <feMergeNode id="feMergeNode3996" in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="filter3998" inkscape:label="Drop shadow" width="1.5" height="1.5" x="-.25" y="-.25">
      <feGaussianBlur id="feGaussianBlur4000" in="SourceAlpha" stdDeviation="1.000000" result="blur"/>
      <feColorMatrix id="feColorMatrix4002" result="bluralpha" type="matrix" values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1.000000 0 "/>
      <feOffset id="feOffset4004" in="bluralpha" dx="0.000000" dy="4.000000" result="offsetBlur"/>
      <feMerge id="feMerge4006">
        <feMergeNode id="feMergeNode4008" in="offsetBlur"/>
        <feMergeNode id="feMergeNode4010" in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient inkscape:collect="always" xlink:href="#linearGradient3636" id="linearGradient3642" x1="698.44312" y1="908.61511" x2="698.44312" y2="1080.0323" gradientUnits="userSpaceOnUse" gradientTransform="matrix(0.99962589,0,0,1,-1.6180943,0)"/>
  </defs>
  <sodipodi:namedview id="base" pagecolor="#ffffff" bordercolor="#666666" borderopacity="1.0" gridtolerance="10000" guidetolerance="10" objecttolerance="10" inkscape:pageopacity="0.0" inkscape:pageshadow="2" inkscape:zoom="0.30925926" inkscape:cx="-551.56629" inkscape:cy="493.75476" inkscape:document-units="px" inkscape:current-layer="layer1" showgrid="false" inkscape:window-width="1855" inkscape:window-height="1056" inkscape:window-x="65" inkscape:window-y="24" inkscape:window-maximized="1"/>
  <metadata id="metadata2388">
    <rdf:RDF>
      <cc:Work rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage"/>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g inkscape:label="Layer 1" inkscape:groupmode="layer" id="layer1" transform="translate(1.9328e-3,0)">
    <rect style="opacity:1;fill:url(#linearGradient3642);fill-opacity:1;stroke:none" id="rect2862" width="1920" height="171.37723" x="-0.0019328" y="908.62274"/>
    <text xml:space="preserve" style="font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;line-height:0%;font-family:'{2}';-inkscape-font-specification:'{2}';text-align:center;writing-mode:lr-tb;text-anchor:middle;fill:#{1};fill-opacity:1;stroke:none;filter:url(#filter3998)" x="961.7674" y="1026.9" id="text2395"><tspan sodipodi:role="line" id="tspan2397" x="961.7674" y="1026.9" style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:82.35334778px;line-height:125%;font-family:'{2}';text-align:center;writing-mode:lr-tb;text-anchor:middle;fill:{1};fill-opacity:1;stroke:none">{0}</tspan></text>
  </g>
</svg> 
'''

template0 = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   version="1.0"
   id="svg2383"
   height="1080"
   width="1920">
  <defs id="defs2385">
      <linearGradient
       id="linearGradient2334">
      <stop
         id="stop2330"
         offset="0"
         style="stop-color:#4400aa;stop-opacity:1;" />
      <stop
         id="stop2332"
         offset="1"
         style="stop-color:#4400aa;stop-opacity:0;" />
    </linearGradient>
    <radialGradient
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.34859156,0,172.53987)"
       r="107.34524"
       fy="264.87202"
       fx="103.56548"
       cy="264.87202"
       cx="103.56548"
       id="radialGradient2336"
       xlink:href="#linearGradient2334" />

    <linearGradient id="linearGradient3636">
      <stop
         id="stop3638"
         offset="0"
         style="stop-color:#000000;stop-opacity:0.5" />
      <stop
         id="stop3640"
         offset="1"
         style="stop-color:#000000;stop-opacity:0.85" />
    </linearGradient>
    <linearGradient id="linearGradient3670">
      <stop
         style="stop-color:#dcaa38;stop-opacity:1"
         offset="0"
         id="stop3672"/>
      <stop
         style="stop-color:#f4c54f;stop-opacity:1"
         offset="1"
         id="stop3674"/>
    </linearGradient>
    <radialGradient
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1,0,0,0.05818239,-200.15323,977.43371)"
       r="638"
       fy="400"
       fx="1520"
       cy="400"
       cx="1520"
       id="subtitleFgGradient"
       xlink:href="#linearGradient3670"/>
    <linearGradient
       gradientTransform="matrix(0.99962589,0,0,1,-1.6180943,0)"
       gradientUnits="userSpaceOnUse"
       y1="880"
       x1="0"
       y2="1080"
       x2="0"
       id="subtitleBgGradient"
       xlink:href="#linearGradient3636"/>
  </defs>
  <metadata id="metadata2388">
    <rdf:RDF>
      <cc:Work rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage"/>
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g id="layer1">
    <rect
       y="910"
       x="0"
       height="170"
       width="1920"
       id="rect2862"
       style="opacity:1;fill:url(#subtitleBgGradient);fill-opacity:1;stroke:none"/>
    <text id="text2395">
       <tspan
         style="font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:84px;line-height:125%;font-family:'{2}';text-align:center;writing-mode:lr-tb;text-anchor:middle;fill:#ffdd00;fill-opacity:1;stroke:none"
         y="1020"
         x="961"
         id="tspan2397">{0}</tspan></text>
  </g>
</svg>
'''
splitLen = 1          # separators per output file
separator = '\n'    # assumes text has blank line between items

# This is shorthand and not friendly with memory
# on very large files, but it works.
input = open(args.input, 'r').read().split(separator)

at = 1
for lines in range(0, len(input), splitLen):
    # First, get list slice, convert to string and strip whitespace
    outputData = ''.join(input[lines:lines+splitLen]).strip()

    # if line is not empty or a comment
    if len(outputData) > 0 and outputData[0] != '#':
        # Now open the output file using zfill to ensure always same length...
        output = open(args.output + str(at).zfill(2) + '.svg', 'w')
        # ... manipulate, format and write text ...
        output.write(template.format(outputData.strip(), args.color, args.font))
        # ... and close the file.
        output.close()

        # Increment the counter
        at += 1
