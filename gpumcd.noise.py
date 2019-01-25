#!/usr/bin/env python3
import argparse,numpy as np,image

# parser = argparse.ArgumentParser(description='Generate image with noise.')
# #parser.add_argument('indir', nargs='*')
# parser.add_argument('--mean', action='store_true')
# parser.add_argument('--perc', action='store_true')
# opt = parser.parse_args()

noiselevels = [0.2,0.5,1.0,2.0,5.0]

im_artificial_noise=[]
im_gpumcd_noise=[]

for nlevel in noiselevels:
    im_artificial_noise.append(image.image('',DimSize=[50,50,50],ElementSpacing=[2,2,2]))
    im_artificial_noise[-1].fill_gaussian_noise(1000, nlevel)
    im_artificial_noise[-1].saveas(r'D:\postdoc\analyses\unc_study\noise'+str(nlevel)+'.mhd')

    artnoise = im_artificial_noise[-1].get_profiles_at_index(im_artificial_noise[-1].get_pixel_index([0,-30,0],True))

    im_gpumcd_noise.append(image.image(r'D:\postdoc\analyses\unc_study\pc'+str(nlevel)+r'\gpumcd.mhd'))

    gpunoise = im_gpumcd_noise[-1].get_profiles_at_index(im_gpumcd_noise[-1].get_pixel_index([0,-30,0],True))

    for aa,gg in zip(artnoise,gpunoise):
        a = aa[round(len(aa)/3):round(2*len(aa)/3)]
        g = gg[round(len(gg)/3):round(2*len(gg)/3)]
        print("for noiselevel",nlevel,":")
        print("artificial noise (std/mean):",np.std(a)/np.mean(a)*100.)
        print("gpumcd noise (std/mean):",np.std(g)/np.mean(g)*100.)
        break