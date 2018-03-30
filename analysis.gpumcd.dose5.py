#!/usr/bin/env python3
import plot,os,image,numpy as np,random

#rundir = os.path.join(r"Z:\brent\dosia_dump",'8903804','20Gy.trialname.1.beam')
#rundir = r"Z:\brent\dosia_validatiedump\F180220C\6MV_COM.trialname.1.beam"
rundir = r"Z:\brent\dosia_validatiedump\AA171214\Epid_6MV_COM.trialname.1.beam"

images = [image.image(os.path.join(rundir,'dose.mhd')),
image.image(os.path.join(rundir,'gpumcd_dose_water.mhd')), #dose to water, propagate water
image.image(os.path.join(rundir,'gpumcd_dose_inaqua.mhd')), #dose to water, propagate medium
image.image(os.path.join(rundir,'gpumcd_dose.mhd'))
]

names = ['TPS',
       'GPUMCD_water_water',
       'GPUMCD_in_aqua',
       'GPUMCD_medium_medium'
       ]

xsize1 = np.linspace( 0, int( images[0].header['ElementSpacing'][0]*images[0].header['DimSize'][0] ), images[0].header['DimSize'][0] )
xsize2 = np.linspace( 0, int( images[2].header['ElementSpacing'][2]*images[2].header['DimSize'][2] ), images[2].header['DimSize'][2] )

f, (row1,row21,row2,row22,row3,row23) = plot.subplots(nrows=6, ncols=3, sharex=False, sharey=False)

lw=0.4

for im,leg in zip( [images[0],images[3]], [names[0],names[3]] ):
    col=random.choice(plot.colors)
    row1[0].plot(xsize1,im.getline('y'),alpha=0.5,color=col,label=leg,lw=lw)
    row1[1].plot(xsize1,im.getline('z'),alpha=0.5,color=col,label=leg,lw=lw)
    row1[2].plot(xsize2,im.getline('x'),alpha=0.5,color=col,label=leg,lw=lw)

for row,crush,xax in zip( [row21[0],row21[1],row21[2]] , [[1,0,1],[0,1,1],[1,1,0]] , [xsize1,xsize1,xsize2] ):
    tps = images[0].getline(crush)
    gpumcd = images[3].getline(crush)
    row.plot(xax, (gpumcd-tps)/tps ,alpha=0.5,color=col,lw=lw)
    row.set_ylim([-1,1])

#row21[0].plot(xsize1,images[3].get1dlist([1,0,1])/images[0].get1dlist([1,0,1]),alpha=0.5,color=col,lw=lw)
#row21[1].plot(xsize1,images[3].get1dlist([0,1,1])/images[0].get1dlist([0,1,1]),alpha=0.5,color=col,lw=lw)
#row21[2].plot(xsize2,images[3].get1dlist([1,1,0])/images[0].get1dlist([1,1,0]),alpha=0.5,color=col,lw=lw)

for im,leg in zip( [images[0],images[2]], [names[0],names[2]] ):
    col=random.choice(plot.colors)
    row2[0].plot(xsize1,im.getline('y'),alpha=0.5,color=col,label=leg,lw=lw)
    row2[1].plot(xsize1,im.getline('z'),alpha=0.5,color=col,label=leg,lw=lw)
    row2[2].plot(xsize2,im.getline('x'),alpha=0.5,color=col,label=leg,lw=lw)

for row,crush,xax in zip( [row22[0],row22[1],row22[2]] , [[1,0,1],[0,1,1],[1,1,0]] , [xsize1,xsize1,xsize2] ):
    tps = images[0].getline(crush)
    gpumcd = images[2].getline(crush)
    row.plot(xax, (gpumcd-tps)/tps ,alpha=0.5,color=col,lw=lw)
    row.set_ylim([-1,1])

    #row22[0].plot(xsize1,im.get1dlist([1,0,1]),alpha=0.5,color=col,label=leg,lw=lw)
    #row22[1].plot(xsize1,im.get1dlist([0,1,1]),alpha=0.5,color=col,label=leg,lw=lw)
    #row22[2].plot(xsize2,im.get1dlist([1,1,0]),alpha=0.5,color=col,label=leg,lw=lw)
for im,leg in zip( [images[0],images[1]], [names[0],names[1]] ):
    col=random.choice(plot.colors)
    row3[0].plot(xsize1,im.getline('y'),alpha=0.5,color=col,label=leg,lw=lw)
    row3[1].plot(xsize1,im.getline('z'),alpha=0.5,color=col,label=leg,lw=lw)
    row3[2].plot(xsize2,im.getline('x'),alpha=0.5,color=col,label=leg,lw=lw)
    
for row,crush,xax in zip( [row23[0],row23[1],row23[2]] , [[1,0,1],[0,1,1],[1,1,0]] , [xsize1,xsize1,xsize2] ):
    tps = images[0].getline(crush)
    gpumcd = images[1].getline(crush)
    row.plot(xax, (gpumcd-tps)/tps ,alpha=0.5,color=col,lw=lw)
    row.set_ylim([-1,1])

    #row23[0].plot(xsize1,im.get1dlist([1,0,1]),alpha=0.5,color=col,label=leg,lw=lw)
    #row23[1].plot(xsize1,im.get1dlist([0,1,1]),alpha=0.5,color=col,label=leg,lw=lw)
    #row23[2].plot(xsize2,im.get1dlist([1,1,0]),alpha=0.5,color=col,label=leg,lw=lw)
    

row1[0].set_title('PDD')
row1[1].set_title('Profile')
row23[0].set_xlabel('Axis [mm]')
row23[1].set_xlabel('Axis [mm]')
for row in (row1,row2,row3):
    row[0].set_ylabel('Dose [cGy]')
    row[1].set_ylabel('Dose [cGy]')
    row[0].set_xlabel('Axis [mm]')
    row[1].set_xlabel('Axis [mm]')
    row[1].legend(loc='upper right', bbox_to_anchor=(1.2, 1.),frameon=False)

f.savefig(os.path.join(rundir,'dose_prof_pdd.pdf'), bbox_inches='tight')
f.savefig(os.path.join(rundir,'dose_prof_pdd.png'), bbox_inches='tight',dpi=300)

plot.close('all')
