#!/usr/bin/env python3
import sys,image

infile = sys.argv[-1]
img = image.image(infile)
#data = numpy.fromfile(filename, dtype='<f4')

print(img.imdata.sum())