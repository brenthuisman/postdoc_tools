#!/usr/bin/env python3
import image,sys

crush = [1,1,0,1]
infile = sys.argv[-1] #in goes mhd
outpostfix = ".z"

print('Processing', infile, file=sys.stderr)

img = image.image(infile)
img.saveprojection(outpostfix, crush)
