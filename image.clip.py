#!/usr/bin/env python3
import image,sys,numpy

infile = sys.argv[-1] #in goes mhd

print('Processing', infile, file=sys.stderr)

print("This tool will limit the range of indices in this image to the -1000,3000 interval. ONLY USE ON CT IMAGES.")

img = image.image(infile)
img.clip_range(-1000,3000)
print("new min",numpy.nanmin(img.imdata), ", new max",numpy.nanmax(img.imdata))
img.saveas(".clipped")