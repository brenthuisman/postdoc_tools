#!/usr/bin/env python3
import plot,os,image,numpy as np

#rundir = os.path.join(r"Z:\brent\dosia_dump",'8903804','20Gy.trialname.1.beam')
rundir = r"Z:\brent\dosia_validatiedump\F180220C\6MV_COM.trialname.1.beam"
local_pinnacle_dir = r"Z:\brent\pinnacle_dump"
dt='<f4'

#gpudose = image.image(os.path.join(rundir,'gpumcd_dose.mhd'))
dosediff = image.image(os.path.join(rundir,'dosediff.mhd'))
reldosediff = image.image(os.path.join(rundir,'reldosediff.mhd'))
#tpsdose = np.fromfile(os.path.join(rundir,'dose.raw'), dtype=dt)

dosediff = dosediff.imdata.flatten()
reldosediff = reldosediff.imdata.flatten()

#reldosediff=[1,2,3]*40
reldosediff[reldosediff == np.inf]=0
reldosediff[reldosediff == np.nan]=0
#reldosediff[reldosediff >2.]=0
#reldosediff[reldosediff <-1.]=0

f, (ax1,ax2) = plot.subplots(nrows=1, ncols=2, sharex=False, sharey=False)
n = max(plot.plot1dhist(ax1,dosediff))
plot.label_percentile(ax1,dosediff,n,perc=[2],label=False)
plot.label_percentile(ax1,dosediff,n,perc=[98],label=False)
ax1.axvline(np.mean(dosediff), color='#999999', ls='--')
ax1.text(np.mean(dosediff), n,'Mean: '+plot.sn(np.mean(dosediff))+'cGy')

n = max(plot.plot1dhist(ax2,dosediff))
plot.label_percentile(ax2,dosediff,n,perc=[2],label=False)
plot.label_percentile(ax2,dosediff,n,perc=[98],label=False)
ax2.axvline(np.mean(dosediff), color='#999999', ls='--')
ax2.text(np.mean(dosediff), n,'Mean: '+plot.sn(np.mean(dosediff))+'cGy')

ax1.set_yscale('log')
ax1.set_xlabel('Abs. dose diff. [cGy]')
ax2.set_xlabel('Abs. dose diff. [cGy]')
ax1.set_ylabel('Voxels (log)')
ax2.set_ylabel('Voxels')
ax1.set_title('Log absolute dose diff ('+plot.sn(len(dosediff))+' voxels)')
ax2.set_title('Absolute dose diff ('+plot.sn(len(dosediff))+' voxels)')

#ax1.set_title(str(sqlcount)+' SQL records (Agility, nonFFF, 6MV, 16H2-17H1)')
f.savefig(os.path.join(rundir,'dosehist1.pdf'), bbox_inches='tight')
f.savefig(os.path.join(rundir,'dosehist1.png'), bbox_inches='tight',dpi=300)

plot.close('all')
##########################################################
# reldose

f2, (ax3,ax4) = plot.subplots(nrows=1, ncols=2, sharex=False, sharey=False)
n = max(plot.plot1dhist(ax3,reldosediff))#,bins=np.linspace(-1,1,40)))
plot.label_percentile(ax3,reldosediff,n,perc=[2],label=False)
plot.label_percentile(ax3,reldosediff,n,perc=[98],label=False)
ax3.axvline(np.mean(reldosediff), color='#999999', ls='--')
ax3.text(np.mean(reldosediff), n,'Mean: '+plot.sn(np.mean(reldosediff))+'cGy')

n = max(plot.plot1dhist(ax4,reldosediff))
plot.label_percentile(ax4,reldosediff,n,perc=[2],label=False)
plot.label_percentile(ax4,reldosediff,n,perc=[98],label=False)
ax4.axvline(np.mean(reldosediff), color='#999999', ls='--')
ax4.text(np.mean(reldosediff), n,'Mean: '+plot.sn(np.mean(reldosediff))+'cGy')

ax3.set_yscale('log')
ax3.set_xlabel('Abs. dose diff. [cGy]')
ax4.set_xlabel('Abs. dose diff. [cGy]')
ax3.set_ylabel('Voxels (log)')
ax4.set_ylabel('Voxels')
ax3.set_title('Log absolute dose diff ('+plot.sn(len(reldosediff))+' voxels)')
ax4.set_title('Absolute dose diff ('+plot.sn(len(reldosediff))+' voxels)')

f2.savefig(os.path.join(rundir,'dosehist2.pdf'), bbox_inches='tight')
f2.savefig(os.path.join(rundir,'dosehist2.png'), bbox_inches='tight',dpi=300)

plot.close('all')

#for root,dirs,files in os.walk(dosia_dump):
    #if root.count(os.sep) == dosia_dump.count(os.sep) + 2:
        #with open(os.path.join(root,'gammaresult.txt'),'r') as gammaresult:
            #for line in gammaresult:
                #pass
