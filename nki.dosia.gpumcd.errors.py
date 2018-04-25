#!/usr/bin/env python3
import plot,os
from collections import Counter as cntr

dosia_dump = r"Z:\brent\dosia_dump"
local_pinnacle_dir = r"Z:\brent\pinnacle_dump"

errdict = {'-1': "Unknown Error",
           '1': "Ini file missing/corrupt",
           '2': "No commandline argument for input dir provided",
           
           '14': "Failed to load dumpfile",
           
           '20': "dbtype missing",
           '21': "Unknown energy",
           '22': "Unknown beamtype",
           '23': "Unknown filter",
           '27': "Undefined accelerator",
           
           '30': "GpumcdLibrary init fail",
           '31': "MLCi80 encountered",
           '32': "No MachineFile for this Machine",
           '33': "GpumcdLibrary stream init fail",
           '34': "Error reading MachineFile",
           '39': "GpumcdLibrary stream, no output",
           
           '43': "hu2density missing",
           '44': "hu2material missing",
           '45': "density2material missing",
               
           '70': "Problem writing vector to file",
           '71': "Problem writing stringvector to file",
           '71': "Problem reading vector from file",
           
           'sql': 'SQL records',
           'purl': 'Pinnacle URLs'
           }

#################################################################################

errors=[]
newfile=''

with open(os.path.join(local_pinnacle_dir,"purls.txt"),'r') as run_fails:
    for line in run_fails:
        errors.append( 'purl' )
        
with open(os.path.join(dosia_dump,"run_fails.txt"),'r') as run_fails:
    for line in run_fails:
        newfile = line.split(dosia_dump)
#print(newfile)
for line in newfile:
    #print(line)
    try:
        print(line.split()[-1])
        errors.append( line.split()[-1] )
    except IndexError:
        pass

sqlcount=0
with open(os.path.join(local_pinnacle_dir,"sql.results"),'r') as run_fails:
    for line in run_fails:
        sqlcount+=1
        
        
#print(errors)

f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
plot.plotbar(ax1, errors, relabel=errdict)
ax1.set_title(str(sqlcount)+' SQL records (Agility, nonFFF, 6MV, 16H2-17H1)')
f.savefig(os.path.join(dosia_dump,'gpumcderrors.pdf'), bbox_inches='tight')
f.savefig(os.path.join(dosia_dump,'gpumcderrors.png'), bbox_inches='tight',dpi=300)

plot.close('all')



#for root,dirs,files in os.walk(dosia_dump):
    #if root.count(os.sep) == dosia_dump.count(os.sep) + 2:
        #with open(os.path.join(root,'gammaresult.txt'),'r') as gammaresult:
            #for line in gammaresult:
                #pass
