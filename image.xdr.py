#!/usr/bin/env python3
import image,sys,numpy

im = image.image(r"Z:\brent\fieldseries\F180813B\6MV.trialname.4.beam\dose.xdr")
# print(im.imdata.dtype.char)
# print(im.imdata.dtype)
# print(im.imdata.dtype.byteorder) #will say system native before saying BE/LE.
# print(im.imdata.dtype.itemsize)

im.saveas('testxdr.mhd')

im2 = image.image(r"Z:\brent\fieldseries\F180813B\6MV.trialname.4.beam\dose.mhd")
im2.saveas('testmhd.xdr')
# arr = xdr.read(r"Z:\brent\fieldseries\F180813B\6MV.trialname.1.beam\dose.xdr")

# print(arr)
# print(arr.shape)

# xdr.write(r'd:\hoe-rah.xdr',arr)