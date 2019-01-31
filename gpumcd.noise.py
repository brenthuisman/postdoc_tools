#!/usr/bin/env python3
import argparse,numpy as np
import image
from nki import runners

# parser = argparse.ArgumentParser(description='Generate image with noise.')
# #parser.add_argument('indir', nargs='*')
# parser.add_argument('--mean', action='store_true')
# parser.add_argument('--perc', action='store_true')
# opt = parser.parse_args()

rungpu=False

noiselevels = [0.2,0.5,1.0,2.0,5.0]
realisations = 10

if rungpu:
	for nlevel in noiselevels:
		for real in range(realisations):
			im_art=image.image('',DimSize=[50,50,50],ElementSpacing=[2,2,2])
			im_art.fill_gaussian_noise(1000, nlevel)
			im_art.saveas(r'D:\postdoc\analyses\unc_study\artnoise'+str(nlevel)+'_'+str(real)+'.xdr')

			outname = r'D:\postdoc\analyses\unc_study\gpunoise' + str(nlevel)+'_'+str(real)+'.xdr'
			runners.execute(r"D:\postdoc\analyses\unc_study\BeamletLibraryConsumer\x64\Release\BeamletLibraryConsumer.exe","-o \""+outname+"\" -p "+str(nlevel))


gammaresult=[]

artnoiseresult=[]
gpunoiseresult=[]

for nlevel in noiselevels:
	print(nlevel)
	im_artificial_noise=[]
	im_gpumcd_noise=[]
	for real in range(realisations):
		artfname = r'D:\postdoc\analyses\unc_study\artnoise'+str(nlevel)+'_'+str(real)+'.xdr'
		gpufname = r'D:\postdoc\analyses\unc_study\gpunoise'+str(nlevel)+'_'+str(real)+'.xdr'
		masked_artfname = r'D:\postdoc\analyses\unc_study\artnoise'+str(nlevel)+'_'+str(real)+'.masked.xdr'
		masked_gpufname = r'D:\postdoc\analyses\unc_study\gpunoise'+str(nlevel)+'_'+str(real)+'.masked.xdr'
		im_artificial_noise.append( image.image( artfname ) )
		im_gpumcd_noise.append( image.image( gpufname ) )

		mask = image.image( gpufname )
		mask.tomask_atvolume(10)
		im_artificial_noise[-1].applymask(mask)
		im_gpumcd_noise[-1].applymask(mask)

		im_artificial_noise[-1].saveas(masked_artfname)
		im_gpumcd_noise[-1].saveas(masked_gpufname)

		#gammaresult.append(runners.comparedose(masked_artfname,masked_gpufname))

		artn = im_artificial_noise[-1].std()/im_artificial_noise[-1].mean()
		gpun = im_gpumcd_noise[-1].std()/im_gpumcd_noise[-1].mean()
		print("artificial noise (std/mean):",artn)
		print("gpumcd noise (std/mean):",gpun)

		# artnoise = im_artificial_noise[-1].get_profiles_at_index(im_artificial_noise[-1].get_pixel_index([0,-30,0],True))
		# gpunoise = im_gpumcd_noise[-1].get_profiles_at_index(im_gpumcd_noise[-1].get_pixel_index([0,-30,0],True))

		# for aa,gg in zip(artnoise,gpunoise):
		# 	a = aa[round(len(aa)/3):round(2*len(aa)/3)]
		# 	g = gg[round(len(gg)/3):round(2*len(gg)/3)]
		# 	print("for noiselevel",nlevel,":")
		# 	print("profile artificial noise (std/mean):",np.nanstd(a)/np.nanmean(a)*100.)
		# 	print("profile gpumcd noise (std/mean):",np.nanstd(g)/np.nanmean(g)*100.)
		# 	break
