#!/usr/bin/env python3
import argparse,numpy as np
import seaborn as sns,matplotlib.pyplot as plt,scipy.stats as stats
import image
from nki import runners

# parser = argparse.ArgumentParser(description='Generate image with noise.')
# #parser.add_argument('indir', nargs='*')
# parser.add_argument('--mean', action='store_true')
# parser.add_argument('--perc', action='store_true')
# opt = parser.parse_args()

dose_threshold = 50 #in percentage volume

rungpu=False

noiselevels = [0.2,0.5,1.0,2.0,5.0]
# noiselevels = [5.0]
realisations = 10
# realisations =1

if rungpu:
	for nlevel in noiselevels:
		for real in range(realisations):
			im_art=image.image('',DimSize=[50,50,50],ElementSpacing=[2,2,2])
			im_art.fill_gaussian_noise(1000, nlevel)
			im_art.saveas(r'D:\postdoc\analyses\unc_study\artnoise'+str(nlevel)+'_'+str(real)+'.xdr')

			outname = r'D:\postdoc\analyses\unc_study\gpunoise' + str(nlevel)+'_'+str(real)+'.xdr'
			runners.execute(r"D:\postdoc\analyses\unc_study\BeamletLibraryConsumer\x64\Release\BeamletLibraryConsumer.exe","-o \""+outname+"\" -p "+str(nlevel))



mask = image.image( r"D:\postdoc\analyses\unc_study\gpunoise0.2_0.xdr" )
mask.tomask_atvolume(dose_threshold)

for nlevel in noiselevels:
	print(nlevel)
	gammaresult=[]
	imdata_artificial_noise=[]
	imdata_gpumcd_noise=[]
	for real in range(realisations):
		artfname = r'D:\postdoc\analyses\unc_study\artnoise'+str(nlevel)+'_'+str(real)+'.xdr'
		gpufname = r'D:\postdoc\analyses\unc_study\gpunoise'+str(nlevel)+'_'+str(real)+'.xdr'
		masked_artfname = r'D:\postdoc\analyses\unc_study\artnoise'+str(nlevel)+'_'+str(real)+'.masked.xdr'
		masked_gpufname = r'D:\postdoc\analyses\unc_study\gpunoise'+str(nlevel)+'_'+str(real)+'.masked.xdr'


		im_artificial_noise = image.image( artfname )
		im_gpumcd_noise = image.image( gpufname )

		im_artificial_noise.applymask(mask)
		im_gpumcd_noise.applymask(mask)

		# im_artificial_noise.saveas(masked_artfname)
		# im_gpumcd_noise.saveas(masked_gpufname)

		# gammaresult.append(runners.comparedose(masked_artfname,masked_gpufname))

		artn = im_artificial_noise.relunc()
		gpun = im_gpumcd_noise.relunc()
		# print("artificial noise (relunc):",artn*100)
		# print("gpumcd noise (relunc):",gpun*100)

		imdata_artificial_noise.append(im_artificial_noise.imdata.compressed())
		imdata_gpumcd_noise.append(im_gpumcd_noise.imdata.compressed())

	imdata_artificial_noise=np.stack(tuple(imdata_artificial_noise)).T
	imdata_gpumcd_noise=np.stack(tuple(imdata_gpumcd_noise)).T

	ameans=[]
	gmeans=[]

	avars=[]
	gvars=[]

	astds=[]
	gstds=[]

	arelunc=[]
	grelunc=[]

	for bina,bing in zip(imdata_artificial_noise,imdata_gpumcd_noise):
		ameans.append(np.nanmean(bina))
		gmeans.append(np.nanmean(bing))

		# astds.append(np.nanstd(bina))
		# gstds.append(np.nanstd(bing))

		avars.append(np.nanvar(bina))
		gvars.append(np.nanvar(bing))

		arelunc.append((np.nanstd(bina)/np.nanmean(bina))*100)
		grelunc.append((np.nanstd(bing)/np.nanmean(bing))*100)

	amean = np.mean(ameans)
	gmean = np.mean(gmeans)

	astd = np.sqrt(np.mean(avars))*100
	gstd = np.sqrt(np.mean(gvars))*100

	print("artificial noise:")
	print("mean mean:",amean)
	print("mean std:",astd)
	print("mean relunc:",astd/amean)
	print("gpumcd noise:")
	print("mean mean:",gmean)
	print("mean std:",gstd)
	print("mean relunc:",gstd/gmean)

	## plot
	fname = r"D:\postdoc\analyses\unc_study\results\distplot"+str(dose_threshold)+'_'+str(nlevel)
	sns.set_style(style="whitegrid")
	sns.set(font_scale=1.1)

	f, (ax1,ax2) = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=False)
	sns.distplot(arelunc,ax=ax1,kde=False,fit=stats.norm,axlabel="relative uncertainty\nmean: "+str(astd/amean)[:4]+", target: "+str(nlevel))
	sns.distplot(grelunc,ax=ax2,kde=False,fit=stats.norm,axlabel="relative uncertainty\nmean: "+str(gstd/gmean)[:4]+", target: "+str(nlevel))

	ax1.set_title("Artificial noise\nregion: top"+str(dose_threshold)+"%")
	ax2.set_title("GPUMCD noise\nregion: top"+str(dose_threshold)+"%")

	ax1.axvline(astd/amean, ls='--')
	ax2.axvline(gstd/gmean, ls='--')

	# f.subplots_adjust(hspace=.6,wspace=.5)
	f.savefig(fname+'.pdf', bbox_inches='tight')
	# f.savefig(fname+'.png', bbox_inches='tight',dpi=300)













	#print (len(im_artificial_noise))

		# artnoise = im_artificial_noise[-1].get_profiles_at_index(im_artificial_noise[-1].get_pixel_index([0,-30,0],True))
		# gpunoise = im_gpumcd_noise[-1].get_profiles_at_index(im_gpumcd_noise[-1].get_pixel_index([0,-30,0],True))

		# for aa,gg in zip(artnoise,gpunoise):
		# 	a = aa[round(len(aa)/3):round(2*len(aa)/3)]
		# 	g = gg[round(len(gg)/3):round(2*len(gg)/3)]
		# 	print("for noiselevel",nlevel,":")
		# 	print("profile artificial noise (std/mean):",np.nanstd(a)/np.nanmean(a)*100.)
		# 	print("profile gpumcd noise (std/mean):",np.nanstd(g)/np.nanmean(g)*100.)
		# 	break
