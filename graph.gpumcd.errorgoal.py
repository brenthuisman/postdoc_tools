#!/usr/bin/env python3
import numpy as np,matplotlib as mpl,plot,math
clrs=plot.colors

f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)

x = range(1,125)

def targeterr(cpi, prec):
    retval = prec
    if cpi>3:
        retval *= math.sqrt(float(cpi))/2.
    if retval > 10.:
        return 10.
    else:
        return retval


ax1.set_title('GPUMCD Error Goal per Control Point')
ax1.set_xlabel('# CPs')
ax1.set_ylabel('Target Error / CP [%]')
ax1.plot(x, [math.sqrt(i) for i in x],'-',color=clrs[0],lw=0.3,label='Theory HP')
ax1.plot(x, [targeterr(i,1.) for i in x],'-',color=clrs[0],lw=1,label='High Precision')
ax1.plot(x, [1+math.sqrt(i) for i in x],'-',color=clrs[1],lw=0.3,label='Theory NP')
ax1.plot(x, [targeterr(i,2.) for i in x],'-',color=clrs[1],lw=1,label='Normal precision')
#ax2 = ax1.twinx()
#ax2.plot(x, [i/j*100.-100. for i,j in zip(cpu,gpu)],color=clrs[2],lw=1,label='GPU speed advantage')
#ax2.set_ylabel('Speed up (+%)')
ax1.legend(loc='upper left', frameon=False)
#ax2.legend(loc='upper right', bbox_to_anchor=(1., 1.),frameon=False)
#ax1.set_ylim(bottom=0.)

#ax9.set_title('Cost')
#ax9.set_xlabel('Streams')
#ax9.set_ylabel('Runtime [s]')
#plot.plotbar(ax9,cpu_equiv+gpu_equiv)

plot.texax(ax1)
#plot.texax(ax2)
f.savefig('gpumcdtargeterror.pdf', bbox_inches='tight')

plot.close('all')

