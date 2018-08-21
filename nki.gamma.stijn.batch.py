import subprocess,collections,os,glob,plot

#######################################

gammatool = r"D:\postdoc\code\DoseCompareCmdline\src\Win32\Debug\dosecompare_cmd.exe"
local_dose_dir = r"Z:\brent\stijn\dicom"
#dta = 3 #in mm
#perc = 3 #perc...
#localgamma = True
#isodose = 50 #region where to gather gamma stats, in perc
flat=False
showoutliers = False

#######################################

pinim = sorted(glob.glob(local_dose_dir+"/*pin.xdr"), recursive=True)
monim = sorted(glob.glob(local_dose_dir+"/*mon.xdr"), recursive=True)

results=[]

if os.path.isfile(os.path.join(local_dose_dir,'gammaresults.txt')):
    print("Exisiting gammaresults.txt found, skipping analysis...")
    with open(os.path.join(local_dose_dir,'gammaresults.txt'),'r') as resultfile:
        results=resultfile.readlines()
else:
    for i,j in zip(pinim,monim):
        cmd = gammatool+' /dose1 '+i+' /dose2 '+j+' /outgamma '+i.split('pin')[0]+'gamma.xdr'
        #print(cmd)
        result = subprocess.check_output(cmd).decode('utf-8').strip()
        print(result)
        results.append(result+'\n')


    with open(os.path.join(local_dose_dir,'gammaresults.txt'),'w') as resultfile:
        resultfile.writelines(results)

data = collections.defaultdict(list)
for line in results:
    for item in line.split():
        data[item.split('=')[0]].append(float(item.split('=')[-1]))

if flat:
    f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
    ax1.boxplot( data.values() , labels=data.keys() , showfliers=showoutliers )
else:
    f, axes = plot.subplots(nrows=2, ncols=3, sharex=False, sharey=False)
    for index,(dat,val) in enumerate(zip(data.values(),data.keys())):
        axes[ index//3 , index%3 ].boxplot( dat , showfliers=showoutliers )
        axes[ index//3 , index%3 ].set_title(val)


f.savefig(os.path.join(local_dose_dir,'gammaanalysis.pdf'), bbox_inches='tight')
f.savefig(os.path.join(local_dose_dir,'gammaanalysis.png'), bbox_inches='tight',dpi=300)
plot.close('all')

