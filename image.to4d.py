#!/usr/bin/env python3
import image,sys

infile = sys.argv[-1] #in goes mhd

print('Processing', infile, file=sys.stderr)

img = image.image(infile)
img.tofake4d()
