#!/usr/bin/env python3
import image,argparse,numpy as np
from os import path

if __name__ == '__main__': #mot voor calc_gamma thread spawner

    parser = argparse.ArgumentParser(description='supply an image and a mask or percentage for isodose contour in which to compute the DVH.')
    parser.add_argument('--ref')
    parser.add_argument('--compare')
    parser.add_argument('--maskimage',default=None)
    parser.add_argument('--maskregion',default=None,type=float)
    opt = parser.parse_args()

    im1 = image.image(path.abspath(opt.ref))
    im2 = image.image(path.abspath(opt.compare))

    maskim = None
    if opt.maskregion == None and path.isfile(path.abspath(opt.maskimage)):
        print('Using',opt.maskimage,'as region for DVH analysis.')
        maskim = image.image(path.abspath(opt.maskimage))
    elif opt.maskregion != None:
        assert 0 < opt.maskregion < 100
        print('Using isodose contour in reference image at',opt.maskregion,'percent of maximum dose as region for gamma analysis.')
        maskim = im1.copy()
        maskim.tomask_atthreshold((opt.maskregion/100.)*maskim.max())

    else:
        print('No mask or maskregion specified; using whole volume for DVH analysis.')

    ga = im1.compute_gamma(im2,3,3)

    if maskim != None:
        ga.applymask(maskim)

    print()
    print("mean,passrate,median,99percentile")
    print(ga.mean(),ga.passrate(),*ga.percentiles([50,99]))

    print(np.nansum(ga.imdata < 1.))
    print(ga.imdata.count())

    ## save last, because it unfortunately converts masked_array to regular ones
    ga.saveas(r'd:\test.mhd')
