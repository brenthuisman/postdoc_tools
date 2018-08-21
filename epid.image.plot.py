#!/usr/bin/env python3
import argparse,numpy as np,matplotlib as mpl,image,plot
from scipy import fftpack
from collections import OrderedDict

parser = argparse.ArgumentParser(description='Plot dose as func of transmission or not.')
parser.add_argument('indir', nargs='*')
parser.add_argument('--tle', action='store_true')
parser.add_argument('--phosphor', action='store_true')
args = parser.parse_args()
indir = args.indir[0].rstrip('/')

outname = 'epid_plot.pdf'
imyields = glob.glob(indir+"/**/epiddose-trans-Dose.mhd", recursive=True)+glob.glob(indir+"/**/epiddose-nontrans-Dose.mhd", recursive=True)+glob.glob(indir+"/**/epiddose-Dose.mhd", recursive=True)
imuncs = glob.glob(indir+"/**/epiddose-trans-Dose-Uncertainty.mhd", recursive=True)+glob.glob(indir+"/**/epiddose-nontrans-Dose-Uncertainty.mhd", recursive=True)+glob.glob(indir+"/**/epiddose-Dose-Uncertainty.mhd", recursive=True)

if args.tle:
    outname = 'epid_tle_plot.pdf'
    imyields = glob.glob(indir+"/**/epiddose-trans-tle-Dose.mhd", recursive=True)+glob.glob(indir+"/**/epiddose-nontrans-tle-Dose.mhd", recursive=True)+glob.glob(indir+"/**/epiddose-tle-Dose.mhd", recursive=True)
    imuncs = glob.glob(indir+"/**/epiddose-trans-tle-Dose-Uncertainty.mhd", recursive=True)+glob.glob(indir+"/**/epiddose-nontrans-tle-Dose-Uncertainty.mhd")+glob.glob(indir+"/**/epiddose-tle-Dose-Uncertainty.mhd", recursive=True)

print(imyields)

labels = ['nontransmission','transmission','total dose'] #(non) transmission swapped, because IT IS KILLED BY THE ACTOR!!!!

fracties_totaal = []
fracties_isocentrum = []

f, axes = plot.subplots(nrows=len(imyields)+1, ncols=4, sharex=False, sharey=False)#,figsize=(28,10))

for axrow,yim,uim,label in zip(axes,imyields,imuncs,labels):
    print(yim,uim,label)
    yim_ = image.image(yim,type='yield')
    uim_ = image.image(uim,type='relunc') #the doseactor outputs relative uncertainties as per Chetty, see GateImageWithStatistic
    #uim_.applymask(mask90pc)
    uim_.imdata = uim_.imdata.squeeze()*100. #fractions to percentages
    fracties_isocentrum.append( yim_.getcenter().mean() )
    fracties_totaal.append( yim_.imdata.sum() )
    axrow[0].imshow( yim_.imdata.squeeze() , extent = [0,41,0,41], cmap='gray')
    axrow[0].set_title(label + '\n$\sum$ Dose: '+ plot.sn(fracties_totaal[-1]))

    axrow[1].set_title(label + ' Profile')
    axrow[1].plot(*yim_.getprofile('y'), color = 'steelblue' , label='x')
    axrow[1].plot(*yim_.getprofile('x'), color = 'indianred' , label='y')
    axrow[1].legend(loc='upper right', bbox_to_anchor=(1., 1.),frameon=False)
    axrow[1].axvline(41./2.-8., color='#999999', ls='--') #10x10 at isoc is 16x16 at epid level
    axrow[1].axvline(41./2.+8., color='#999999', ls='--')
    axrow[1].set_xlim(0,41)
    plot.set_metric_prefix_y(axrow[1])

    axrow[2].set_title(label+' relunc')
    plot.plot1dhist( axrow[2], uim_.imdata.flatten(), bins=np.linspace(0,100,50), log=True)

frac_trans=1.
frac_nontrans=1.
if args.phosphor:
    npart_trans=112525576.
    npart_tot=127153038.
    frac_trans=npart_trans/npart_tot
    frac_nontrans=1.-frac_trans

sumim = image.image(imyields[0],type='yield')
sumim.imdata=sumim.imdata.squeeze()*frac_nontrans+image.image(imyields[1],type='yield').imdata.squeeze()*frac_trans
axes[-1][0].imshow( sumim.imdata , extent = [0,41,0,41], cmap='gray')
axes[-1][0].set_title('Sum' + '\n$\sum$ Dose: '+ plot.sn(sumim.imdata.sum()))

axes[-1][1].set_title('Sum Profile')
axes[-1][1].plot(*sumim.getprofile('y'), color = 'steelblue' , label='x')
axes[-1][1].plot(*sumim.getprofile('x'), color = 'indianred' , label='y')
axes[-1][1].legend(loc='upper right', bbox_to_anchor=(1., 1.),frameon=False)
axes[-1][1].axvline(41./2.-8., color='#999999', ls='--') #10x10 at isoc is 16x16 at epid level
axes[-1][1].axvline(41./2.+8., color='#999999', ls='--')
axes[-1][1].set_xlim(0,41)
plot.set_metric_prefix_y(axes[-1][1])

#axes[-1][2].set_title('Sum relunc')
#plot.plot1dhist( axes[-1][2], sumim.imdata.flatten(), bins=np.linspace(0,100,50), log=True)




staaf = OrderedDict()
for label,ft,fi in zip(labels,fracties_totaal,fracties_isocentrum)[:-1]:
    staaf[label+' whole']=float(ft)/fracties_totaal[-1]*100. #pc
    staaf[label+' isoc']=float(fi)/fracties_isocentrum[-1]*100.
#staaf = [labels[0], fracties_totaal[0]/fracties_totaal[2]
#print fracties_isocentrum[0]/fracties_isocentrum[2]
staaf

plot.plotbar(axes[0][-1],staaf,bincount='%')#,rotation=30)

staaf2 = OrderedDict()
staaf2['sum/all whole']=(fracties_totaal[0]+fracties_totaal[1])/fracties_totaal[2]*100. #pc
staaf2['sum/all isoc']=(fracties_isocentrum[0]+fracties_isocentrum[1])/fracties_isocentrum[2]*100.
plot.plotbar(axes[1][-1],staaf2,bincount='%')



f.subplots_adjust(hspace=.5,wspace=.5)
f.savefig(indir.replace('/','_')+'_'+outname, bbox_inches='tight')
plot.close('all')
