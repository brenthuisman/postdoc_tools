import subprocess,collections,os,glob,plot

#######################################

gammatool = r"D:\postdoc\code\DoseCompareCmdline\src\Win32\Debug\dosecompare_cmd.exe"
local_dose_dir = r"Z:\brent\DataVoorBrent"
dta = 3 #in mm
perc = 3 #perc...
localgamma = True
isodose = 50 #region where to gather gamma stats, in perc
flat=False

#######################################

pinim = sorted(glob.glob(local_dose_dir+"/*pin.xdr"))
monim = sorted(glob.glob(local_dose_dir+"/*mon.xdr"))

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
    ax1.boxplot( data.values() , labels=data.keys() )
else:
    f, axes = plot.subplots(nrows=2, ncols=3, sharex=False, sharey=False)
    for index,(dat,val) in enumerate(zip(data.values(),data.keys())):
        axes[ index//3 , index%3 ].boxplot( dat )
        axes[ index//3 , index%3 ].set_title(val)


f.savefig(os.path.join(local_dose_dir,'gammaanalysis.pdf'), bbox_inches='tight')
f.savefig(os.path.join(local_dose_dir,'gammaanalysis.png'), bbox_inches='tight',dpi=300)
plot.close('all')
















#######################################

"""
## Match42 shite
import importlib.util
spec = importlib.util.spec_from_file_location("M42_Python", "D:\install\Match42\python\M42_Python.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)

from M42_Python import *


def readdose(Filename, Dose):
    READ_XDR(Dose,FileName)
    FIELD_TO_FLOAT(Dose,Dose)

    Xfm = TAVSField.Create()
    READ_XDR(Xfm,FileName.split('.')[0]+'_xfm.xdr')

    ##new grid thats uniform

    tmpGrid = TAVSField.Create()
    Corners = TAVSField.Create()
    GET_CORNER_DOTS(Dose, Corners)
    DOTXFM(Corners, Xfm, Corners)
    xmin = Corners.Min_Coord[0]
    ymin = Corners.Min_Coord[1]
    zmin = Corners.Min_Coord[2]
    xmax = Corners.Max_Coord[0]
    ymax = Corners.Max_Coord[1]
    zmax = Corners.Max_Coord[2]
    xnbins=round((xmax-xmin) / 0.2)
    ynbins=round((ymax-ymin) / 0.2)
    znbins=round((zmax-zmin) / 0.2)
    FIELD_GRID(tmpGrid,
            xnbins,
            ynbins,
            znbins,
            xnbins*0.2,
            ynbins*0.2,
            znbins*0.2,
            xmin + ((xmax-xmin)/2),
            ymin + ((ymax-ymin)/2),
            zmin + ((zmax-zmin)/2))
    FIELDXFM(Dose, Xfm, tmpGrid, Dose, 0, 0, FIELDXFM_3Dfield,1)
    
def GetPercentile(Arr,FFraction,fPercentile):
    i = math.floor(FFraction * (High(Arr) + 1)) # High(Arr)+1 is #points
    i = i + 1 # round up to next highest integer
    bold = false
    if not bold then
        i = i - 1 # take that number
    fPercentile = Arr[i]
    
def SortField(fldmaskedgamma, fldmaskselected):
    pfData = fldmaskedgamma.GetDataPointerAt([0])
    nx = fldmaskedgamma.Dimensions[0]
    ny = fldmaskedgamma.Dimensions[1]
    nz = fldmaskedgamma.Dimensions[2]
    if nz = 0 then
        nz = 1
    n = nx * ny * nz
    #SetLength(Arr, n)
    Arr = [None]*n
    for k = 0 to nz - 1:
        for j = 0 to ny - 1:
            for i = 0 to nx - 1:
                Arr[ny * nx * k + nx * j + i] = pfData[0]
                pfData = @pfData[1]
    Arr.sort()#QuickSort(Arr)
    fval = fldmaskselected.Mean * n
    iOffset = round(fval)
    iOffset = n - iOffset # #zeros
    Arr = Copy(Arr, iOffset, n - iOffset)

    
def gammacalc(FDose1,FDose2):
    Gamma1 = TAVSField.Create()
    Gamma2 = TAVSField.Create()
    GammaStatsMaskTmp = TAVSField.Create()
    GammaStatsMask = TAVSField.Create()
    
    FIELD_MAXC(FDose1,FDose1,FDose1.Maximum*0.10)
    FIELD_MAXC(FDose2,FDose2,FDose1.Maximum*0.10)

    ##make new 2mm grid the size of the union of the two dosemaps

    tmpGrid = TAVSField.Create()
    Corners1 = TAVSField.Create()
    Corners2 = TAVSField.Create()
    GET_CORNER_DOTS(FDose1, Corners1)
    GET_CORNER_DOTS(FDose2, Corners2)
    #DOTXFM(Corners, Xfm, Corners)

    xmin = max(Corners1.Min_Coord[0],Corners2.Min_Coord[0])
    ymin = max(Corners1.Min_Coord[1],Corners2.Min_Coord[1])
    zmin = max(Corners1.Min_Coord[2],Corners2.Min_Coord[2])
    xmax = min(Corners1.Max_Coord[0],Corners2.Max_Coord[0])
    ymax = min(Corners1.Max_Coord[1],Corners2.Max_Coord[1])
    zmax = min(Corners1.Max_Coord[2],Corners2.Max_Coord[2])

    xnbins=round((xmax-xmin) / 0.2)
    ynbins=round((ymax-ymin) / 0.2)
    znbins=round((zmax-zmin) / 0.2)
    FIELD_GRID(tmpGrid,
            xnbins,
            ynbins,
            znbins,
            xnbins*0.2,
            ynbins*0.2,
            znbins*0.2,
            xmin + ((xmax-xmin)/2),
            ymin + ((ymax-ymin)/2),
            zmin + ((zmax-zmin)/2))

    FIELDXFM(FDose2, None, tmpGrid, Gamma2, 0, 0,FIELDXFM_3Dfield, 1)
    FIELDXFM(FDose1, None, tmpGrid, Gamma1, 0, 0,FIELDXFM_3Dfield, 1)

    MaxC = 0.001
    MaxDist = 1.0
    Accuracy = 0.1
    Outside = 1000.0

    if MaxC != 0.0:
        FIELD_MAXC(Gamma1, Gamma1, 0.001)
        FIELD_MAXC(Gamma2, Gamma2, 0.001)
    
    NormDose = 0.
    if localgamma:
        NormDose = 0.
    else
        NormDose = (FDose1.Maximum+FDose2.Maximum)/2
    
    DOSE_GAMMA(Gamma1, Gamma2, FGamma, 0.0, 0.3, 10000.0, 1.0, perc / 100.0, dta / 10.0,
    MaxDist, Outside, NormDose, Accuracy)
    
    FIELD_MULC(FGamma, FGamma, 100)
    level = FDose1.Maximum * isodose/100.0

    # 2 stats mask: gamma values only in isodose% of dose1,2
    FldTmp1 = TAVSField.Create()
    FldTmp2 = TAVSField.Create()
    
    FIELDXFM(FDose1, None, FGamma, FldTmp1, 0, 0, FIELDXFM_3Dfield, 1)
    FIELD_GTEC(FldTmp1, FldTmp1, level)
    FIELD_DIVC(FldTmp1, FldTmp1, 255)
    
    FIELDXFM(FDose2, None, FGamma, FldTmp2, 0, 0,FIELDXFM_3Dfield, 1)
    FIELD_GTEC(FldTmp2, FldTmp2, level)
    FIELD_DIVC(FldTmp2, FldTmp2, 255)
    # union of both volumes
    #   FIELD_ADD(FldTmp1, FldTmp2, GammaStatsMask)
    FIELD_COPY(FldTmp1, GammaStatsMask)
    FIELD_GTEC(GammaStatsMask, GammaStatsMask, 1)
    FIELD_DIVC(GammaStatsMask, GammaStatsMask, 255)
    # use then GammaStatsMask for statistics
    FIELD_TO_BYTE(GammaStatsMask, GammaStatsMask, 1, 1, true)
    if GammaStatsMask.Datatype = AVS_TYPE_BYTE:
        FIELD_MASK(FGamma, GammaStatsMask, GammaStatsMaskTmp, 0.0)
    else
        FIELD_MUL(FGamma, GammaStatsMask, GammaStatsMaskTmp)
    
    FreeAndNil(FldTmp2)
    FreeAndNil(FldTmp1)
    
    FldTmp1 = TAVSField.Create()
    FldTmp2 = TAVSField.Create()
    
    FIELD_COPY(GammaStatsMaskTmp, FldTmp1)
    FIELD_TO_FLOAT(GammaStatsMask, FldTmp2)
    FIELD_SUBC(FldTmp2, FldTmp2, 1)
    FIELD_MULC(FldTmp2, FldTmp2, -1E10) # was 10
    FIELD_ADD(FldTmp1, FldTmp2, FldTmp1)
    NSTATS(FldTmp1, FldTmp2, NSTATS_MEAN, 0, 1, 1, 1)
    FIELD_GETVAL(FldTmp2, FMean, 0, 0)
    NSTATS(FldTmp1, FldTmp2, NSTATS_STD, 0, 1, 1, 1)
    FIELD_GETVAL(FldTmp2, FStdev, 0)
    NSTATS(FldTmp1, FldTmp2, NSTATS_Min, 0, 1, 1, 1)
    FIELD_GETVAL(FldTmp2, FMin, 0, 0)
    NSTATS(FldTmp1, FldTmp2, NSTATS_Max, 0, 1, 1, 1)
    FIELD_GETVAL(FldTmp2, FMax, 0, 0)
    FMean = FMean / 100.0
    FStdev = FStdev / 100.0
    FMin = FMin / 100.0
    FMax = FMax / 100.0

    FIELD_LTEC(FldTmp1, FldTmp2, 100.0)
    FIELD_DIVC(FldTmp2, FldTmp2, 255)
    FWithinCriteria = FldTmp2.Mean / GammaStatsMask.Mean
    
    FldTmp1.Free()
    FldTmp2.Free()
    
    DynArrDouble = []
    SortField(GammaStatsMaskTmp, GammaStatsMask, DynArrDouble)
    GetPercentile(DynArrDouble, 0.95, Percentile)
    FP95 = Percentile / 100.0
    GetPercentile(DynArrDouble, 0.99, Percentile)
    FP99 = Percentile / 100.0
    
    FreeAndNil(Gamma1)
    FreeAndNil(Gamma2)
    FreeAndNil(GammaStatsMaskTmp)
    FreeAndNil(GammaStatsMask)
    
    #mmo1.Lines.Add(Format('Mean=%.2f ppc<1=%.2f p99=%.2f p95=%.2f Max=%.2f Min=%.2f',
    #[FMean, FWithinCriteria*100, FP99, FP95, FMax, FMin]))
    
    return 'Mean=%.2f ppc<1=%.2f p99=%.2f p95=%.2f Max=%.2f Min=%.2f' % (FMean, FWithinCriteria*100, FP99, FP95, FMax, FMin)
    
"""
