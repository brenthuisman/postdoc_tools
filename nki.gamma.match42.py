## Match42 shite
import importlib.util
spec = importlib.util.spec_from_file_location("M42_Python", "D:\install\Match42\python\M42_Python.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)

from M42_Python import *

## general imports
import subprocess,collections,os,glob,plot

## params

gammatool = r"D:\postdoc\code\DoseCompareCmdline\src\Win32\Debug\dosecompare_cmd.exe"
#local_dose_dir = r"Z:\brent\dosia_dump"
local_dose_dir = r"Z:\brent\jochempepijn"
#local_dose_dir = r"Z:\brent\stijn\pinnacle_dump"
flat=False
showoutliers = False

#dta = 3 #in mm
#perc = 3 #perc...
#localgamma = True
#isodose = 50 #region where to gather gamma stats, in perc

## sum beam subdirs to whole-fraction

frac_names = [] #keep these parallel
results = []

if os.path.isfile(os.path.join(local_dose_dir,'gammaresults.txt')):
    print("Exisiting gammaresults.txt found, skipping analysis...")
    with open(os.path.join(local_dose_dir,'gammaresults.txt'),'r') as resultfile:
        results=resultfile.readlines()
    for i in range(len(results)):
        results[i] = results[i].split(' ',1)[-1]
else:
    beams = sorted( glob.glob( os.path.join(local_dose_dir,"*/*/gpumcd_dose.xdr") , recursive=True ) )

    fractions = collections.defaultdict(list)

    for beam in beams:
        assert(beam.endswith(".beam\gpumcd_dose.xdr"))
        base = beam[:-33]
        #beamnr = beam[-7]
        fractions[base].append(beam.replace("gpumcd_dose.xdr",""))

    for frac,beams in fractions.items():
        tpsdosesum_fname = frac+'.tps.xdr'
        gpumcddosesum_fname = frac+'.gpumcd.xdr'

        tpsdosesum = TAVSField()
        gpumcddosesum = TAVSField()

        try:
            for i,beam in enumerate(beams):
                tpsdose = TAVSField()
                gpumcddose = TAVSField()

                READ_XDR(tpsdose,beam+"/dose.xdr")
                READ_XDR(gpumcddose,beam+"/gpumcd_dose.xdr")

                if i is 0:
                    FIELD_COPY(tpsdose,tpsdosesum)
                    FIELD_COPY(gpumcddose,gpumcddosesum)
                else:
                    FIELD_ADD(tpsdose,tpsdosesum,tpsdosesum) #3rd arg is output field
                    FIELD_ADD(gpumcddose,gpumcddosesum,gpumcddosesum)

                tpsdose.Free()
                gpumcddose.Free()

        except Exception as e:
            print("AVS Exception occurred.")
            print(frac,beam)
            print("AVS Exception description:")
            print(e)
        WRITE_XDR(tpsdosesum,tpsdosesum_fname)
        WRITE_XDR(gpumcddosesum,gpumcddosesum_fname)

        tpsdosesum.Free()
        gpumcddosesum.Free()

        frac_names.append('\\'.join(frac.split('\\')[-2:]))
        cmd = gammatool+' /dose1 '+tpsdosesum_fname+' /dose2 '+gpumcddosesum_fname+' /outgamma null'
        #print(cmd)
        result = subprocess.check_output(cmd).decode('utf-8').strip()
        print(result)
        results.append(result+'\n')

    with open(os.path.join(local_dose_dir,'gammaresults.txt'),'w') as resultfile:
        resultfile.writelines([i+': '+j for i,j in zip(frac_names,results)])

data = collections.defaultdict(list)
for line in results:
    for item in line.split():
        data[item.split('=')[0]].append(float(item.split('=')[-1]))

if flat:
    f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
    ax1.boxplot( data.values() , labels=data.keys() , showfliers=showoutliers )
    ax1.set_yscale('log')
else:
    f, axes = plot.subplots(nrows=2, ncols=3, sharex=False, sharey=False)
    for index,(dat,val) in enumerate(zip(data.values(),data.keys())):
        axes[ index//3 , index%3 ].boxplot( dat , showfliers=showoutliers )
        axes[ index//3 , index%3 ].set_title(val)
        #axes[ index//3 , index%3 ].set_yscale('log')

f.savefig(os.path.join(local_dose_dir,'gammaanalysis.pdf'), bbox_inches='tight')
f.savefig(os.path.join(local_dose_dir,'gammaanalysis.png'), bbox_inches='tight',dpi=300)
plot.close('all')
