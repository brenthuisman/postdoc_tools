#!/usr/bin/env python3
import image,sys

infile = sys.argv[-1] #in goes mhd
outpostfix = ".2dfront"
crush = [0,0,1,1]

print('Processing', infile, file=sys.stderr)

img = image.image(infile)
img.saveprojection(outpostfix, crush)
