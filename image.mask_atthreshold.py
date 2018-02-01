#!/usr/bin/env python3
import image,sys

infile = sys.argv[-1] #in goes mhd
thres = float(sys.argv[-2])

print('Processing', infile, file=sys.stderr)

img = image.image(infile)
print("Max val in image:",img.imdata.max())
print("Mask at threshold:",thres)
img.savemask_atthreshold(thres)
