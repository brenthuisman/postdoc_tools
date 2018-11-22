#!/usr/bin/env python3
import image,argparse,numpy as np
from os import path

parser = argparse.ArgumentParser(description='supply an image and a mask or percentage for isodose contour in which to compute the DVH.')
parser.add_argument('inputimage')
parser.add_argument('--maskimage',default=None)
parser.add_argument('--isodoseregion',default=None,type=float)
opt = parser.parse_args()

im = image.image(path.abspath(opt.inputimage))
maskim = None

if opt.isodoseregion == None and path.isfile(path.abspath(opt.maskimage)):
    print('Using',opt.maskimage,'as region for DVH analysis.')
    maskim = image.image(path.abspath(opt.maskimage))
elif opt.isodoseregion != None:
    assert 0 < opt.isodoseregion < 100
    print('Using isodose contour at',opt.isodoseregion,'percent of maximum dose as region for DVH analysis.')
    maskim = im.copy()
    maskim.tomask_atthreshold((opt.isodoseregion/100.)*maskim.max())
else:
    print('No mask or isodoseregion specified; using whole volume for DVH analysis.')

if maskim != None:
    im.applymask(maskim)

# note: array is sorted in reverse for DVHs, i.e. compute 100-n%
D2,D50,D98 = im.percentiles([98,50,2])

print("Dmax,D2,D50,D98,Dmean")
print(im.imdata.max(),D2,D50,D98,im.mean())