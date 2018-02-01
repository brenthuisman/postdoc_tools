#!/usr/bin/env python3
import image,argparse,numpy as np

parser = argparse.ArgumentParser(description='secret')
parser.add_argument('--ct')
parser.add_argument('--mask')
parser.add_argument('--frac')
args = parser.parse_args()

tmpval = -7389.

ctim = image.image(str(args.ct))
mskim = image.image(str(args.mask))
assert(ctim.imdata.shape == mskim.imdata.shape)

#binnen = np.ma.masked_where(mskim.imdata == 1., mskim.imdata)
#buiten = np.ma.masked_where(mskim2.imdata == 0., mskim2.imdata)
binnen = np.ma.masked_equal(mskim.imdata, 1.)
buiten = np.ma.masked_equal(mskim.imdata, 0.)


ct_mean = np.ma.masked_array(ctim.imdata, mask=buiten).mean() #daar waar pixel(buiten) = 1: negeer waarden.

#ct_mean = 0.
print('Setting volume in mask to',ct_mean)
print(np.ma.masked_array(ctim.imdata, mask=binnen).mean())

ctim.imdata = np.ma.masked_array(ctim.imdata, mask=binnen).filled(ct_mean)

ctim.saveas('maskedtest')

#ctimmasked = ctim.applymask_clitk('masked',str(args.mask),tmpval) #leaves original unaffected




