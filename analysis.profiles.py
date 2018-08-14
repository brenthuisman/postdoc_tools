#!/usr/bin/env python3
import numpy as np,sys,image,seaborn as sns,plot,argparse,pandas as pd
from os import path
# from nki import runners

imagefiles = [r"Z:\brent\stijn\pindump_nooverrides\MonacoPhantom\A.trialname.1.beam\dose.mhd",r"Z:\brent\stijn\pindump_nooverrides\MonacoPhantom\A.trialname.1.beam\gpumcd_dose.mhd"]

# parser = argparse.ArgumentParser(description='specify mulitple mhd images to analyse')
# parser.add_argument('-i', '--image',action='append')
# args = parser.parse_args()
# imagefiles = args.image

fname = path.join(path.dirname(imagefiles[0]),'profile_plot')
images = [image.image(i) for i in imagefiles]

f, ((ax1,ax2),(ax3,ax4)) = plot.subplots(nrows=2, ncols=2, sharex=False, sharey=False)
sns.set_style("whitegrid")

for im in images:

    sns.lineplot( ax=ax1, y=im.getline('y'), x=im.get_axis_mms('y') ) # PDD == y
    pdd_max = im.getline('y').argmax()
    print('brent',pdd_max)
    sns.lineplot( ax=ax2, y=im.getline_atindex('x',pdd_max), x=im.get_axis_mms('x' ))
    sns.lineplot( ax=ax3, y=im.getline_atindex('z',pdd_max), x=im.get_axis_mms('z') )

reldiff = ( images[1].getline_atindex('x',pdd_max) - images[0].getline_atindex('x',pdd_max) ) / images[1].getline_atindex('x',pdd_max)
sns.lineplot( ax=ax4, y=reldiff, x=im.get_axis_mms('x') )
ax4.fill_between( images[1].get_axis_mms('x'), -0.01, 0.01, alpha=0.3)
ax2.set_xlim(-70,70)
ax3.set_xlim(-70,70)
ax4.set_xlim(-70,70)
ax4.set_ylim(-0.05,0.2)

ax1.set_title("X")
ax2.set_title("Y")
ax3.set_title("Z")
ax4.set_title("reldiff Y")

f.savefig(fname+'.pdf', bbox_inches='tight')
f.savefig(fname+'.png', bbox_inches='tight',dpi=300)

# Finish: stijns profielen
# runners.execute(r"D:\postdoc\code\xdr_xdr2mhd\src\Win32\Debug\xdr_xdr2mhd.exe","/in blabla.xdr")
