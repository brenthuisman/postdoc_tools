#!/usr/bin/env python3
import image,sys

if len(sys.argv) < 3:
	print("Supply an image and a mask.")
	sys.exit()

maskfile = sys.argv[-1] #mask
infile = sys.argv[-2] #image

print('Processing', infile, maskfile, file=sys.stderr)

img = image.image(infile)
msk = image.image(maskfile)
img.applymask(msk)
print(img.getmean())