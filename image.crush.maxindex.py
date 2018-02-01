#!/usr/bin/env python3
import image,sys

infile = sys.argv[-1] #in goes mhd
outpostfix = ".3d"
crush = [0,0,0,1]

print('Processing', infile, file=sys.stderr)

img = image.image(infile)
im3d = img.save_crush_argmax(outpostfix, crush)

outpostfix = ".2dtop"
crush = [0,1,0]
img = image.image(im3d)
img.save_crush_argmax(outpostfix, crush)

outpostfix = ".2dfront"
crush = [1,0,0]
img = image.image(im3d)
img.save_crush_argmax(outpostfix, crush)

outpostfix = ".2dside"
crush = [0,0,1]
img = image.image(im3d)
img.save_crush_argmax(outpostfix, crush)
