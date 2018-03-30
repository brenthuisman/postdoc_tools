#!/usr/bin/env python3
import numpy as np,matplotlib as mpl,plot,sys,re
clrs=plot.colors

f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)

x = [1,2,3,7]

cpu = [174.116,124.691,128.150,133.497]
gpu = [133.161,102.820,94.058,90.751]
#cpu_cost = ['CPU (Threadripper 1920X)']*657
#gpu_cost = ['GPU (Quadro M6000 12GB)']*2406
#ratio_cost = ['Ratio']*2406

ax1.set_title('GPUMCD runtimes')
ax1.set_xlabel('Streams')
ax1.set_ylabel('Runtime [s]')
ax1.plot(x, cpu,color=clrs[0],lw=1,label='CPU (2x XeonE5-2630v3)')
ax1.plot(x, gpu,color=clrs[1],lw=1,label='GPU (1x TitanXp)')
ax2 = ax1.twinx()
ax2.plot(x, [i/j*100.-100. for i,j in zip(cpu,gpu)],color=clrs[2],lw=1,label='GPU speed advantage')
ax2.set_ylabel('Speed up (+%)')
ax1.legend(loc='upper left', frameon=False)
ax2.legend(loc='upper right', bbox_to_anchor=(1., 1.),frameon=False)
ax1.set_ylim(bottom=0.)

#ax9.set_title('Cost')
#ax9.set_xlabel('Streams')
#ax9.set_ylabel('Runtime [s]')
#plot.plotbar(ax9,cpu_equiv+gpu_equiv)

plot.texax(ax1)
#plot.texax(ax2)
f.savefig('gpumcdruntime.pdf', bbox_inches='tight')

plot.close('all')

