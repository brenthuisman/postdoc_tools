#!/usr/bin/env python3
import image,sys,numpy

infile = sys.argv[-1] #in goes mhd

print('Processing', infile, file=sys.stderr)

print("This tool will set all voxel to water (HU=0).")

img = image.image(infile)
img.towater()
img.saveas(".water")
