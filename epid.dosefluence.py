#!/usr/bin/env python3
import argparse,numpy as np,matplotlib as mpl,image,plot,glob

parser = argparse.ArgumentParser(description='Plot dose as func of transmission or not.')
parser.add_argument('--rundir')
#parser.add_argument('--tle', action='store_true')
args = parser.parse_args()
rundir = args.rundir.rstrip('/')

print(rundir)

doseims = glob.glob(rundir+"/**/dose-Dose.mhd")
fluenceims = glob.glob(rundir+"/**/fluence.mhd")

pixels_lowdose = []
pixels_highdose = []
f_voxels = []
d_voxels = []

fielsize_start = 17 #20cm
fielsize_end = 83 #20cm
#fielsize_start = 33 #10cm
#fielsize_end = 67 #10cm
#fielsize_start = 40 #6cm
#fielsize_end = 60 #6cm
#fielsize_start = 43 #3cm
#fielsize_end = 56 #3cm

for d,f in zip(doseims,fluenceims):
	#print (d,f)
	dim = image.image(d)
	fim = image.image(f)
	
	f_voxels += fim.imdata.astype('float').flatten().tolist()
	d_voxels += dim.imdata.astype('float').flatten().tolist()
	
	relim = (dim.imdata.astype('float')/fim.imdata.astype('float')).squeeze()
	
	relim.squeeze()
	relim_highdoseregion=np.copy(relim[fielsize_start:fielsize_end,fielsize_start:fielsize_end])
	relim[fielsize_start:fielsize_end,fielsize_start:fielsize_end]=np.nan
	relim_lowdoseregion = relim[~np.isnan(relim)]
	
	#print(relim.shape)
	#print(relim_highdoseregion.shape)
	#print('Nr of :',np.sum(np.isnan(relim_lowdoseregion)==True))
	#print('Nr of :',np.sum(np.isnan(relim_highdoseregion)==True))
	#quit()
	
	pixels_lowdose += relim_lowdoseregion.flatten().tolist()
	pixels_highdose += relim_highdoseregion.flatten().tolist()
	
assert(len(f_voxels)==len(d_voxels))
ratios = np.array(d_voxels)/np.array(f_voxels)
ratios = ratios[ratios != 0]

#print('Nr of :',np.sum(np.isnan(ratios)==True))
#print('Nr of inf:',np.sum(np.isinf(ratios)==True))
#print(np.min(ratios),np.max(ratios))

f, ((ax1,ax2),(ax3,ax4)) = plot.subplots(nrows=2, ncols=2, sharex=False, sharey=False)#,figsize=(28,10))

plot.plot1dhist_logx(ax1,ratios,edges=[3e-11,1e-9],num=1000)
ax1.axvline(np.median(ratios), color='#999999', ls='--')

plot.plot1dhist_logx(ax2,pixels_lowdose,edges=[3e-11,1e-9],num=1000)
ax2.axvline(np.median(pixels_lowdose), color='#999999', ls='--')

plot.plot1dhist_logx(ax3,pixels_highdose,edges=[3e-11,1e-9],num=1000)
ax3.axvline(np.median(pixels_highdose), color='#999999', ls='--')

plot.plot1dhist_logx(ax4,pixels_highdose,edges=[3e-11,1e-9],num=1000)
ax4.axvline(np.median(pixels_highdose), color='#999999', ls='--')
ax4.set_xlim(np.median(pixels_highdose)/1.2,np.median(pixels_highdose)*1.2)

f.savefig(rundir+'dosefluencehist.pdf', bbox_inches='tight')
plot.close('all')
