## Match42 shite
import importlib.util
spec = importlib.util.spec_from_file_location("M42_Python", "D:\install\Match42\python\M42_Python.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)

from M42_Python import *

## general imports

def readdose(Filename, Dose):
    READ_XDR(Dose,FileName);
    FIELD_TO_FLOAT(Dose,Dose);
    FIELD_MULC(Dose,Dose,Scaling);

    Xfm = TAVSField.Create;
    READ_XDR(Xfm,FileName.Split([Char('.')])[0]+'_xfm.xdr');

    //new grid thats uniform

    //if Grid.Empty then
    //begin
    tmpGrid := TAVSField.Create;
    Corners := TAVSField.Create;
    GET_CORNER_DOTS(Dose, Corners);
    DOTXFM(Corners, Xfm, Corners);
    xmin := Corners.Min_Coord[0];
    ymin := Corners.Min_Coord[1];
    zmin := Corners.Min_Coord[2];
    xmax := Corners.Max_Coord[0];
    ymax := Corners.Max_Coord[1];
    zmax := Corners.Max_Coord[2];
    xnbins:=Round((xmax-xmin) / 0.2);
    ynbins:=Round((ymax-ymin) / 0.2);
    znbins:=Round((zmax-zmin) / 0.2);
    FIELD_GRID(tmpGrid,
            xnbins,
            ynbins,
            znbins,
            xnbins*0.2,
            ynbins*0.2,
            znbins*0.2,
            xmin + ((xmax-xmin)/2),
            ymin + ((ymax-ymin)/2),
            zmin + ((zmax-zmin)/2));
    //end;
    FIELDXFM(Dose, Xfm, tmpGrid, Dose, 0, 0, FIELDXFM_3Dfield,1);
    
def compute_gamma():
Gamma1 := TAVSField.Create;
Gamma2 := TAVSField.Create;
GammaStatsMaskTmp := TAVSField.Create;
GammaStatsMask := TAVSField.Create;
try
FIELD_MAXC(FDose1,FDose1,FDose1.Maximum*0.10);
FIELD_MAXC(FDose2,FDose2,FDose1.Maximum*0.10);
//FIELD_COPY(FDose1,Gamma1);
//FIELD_COPY(FDose2,Gamma2);

//make new grid the size of the union of the two dosemaps

tmpGrid := TAVSField.Create;
Corners1 := TAVSField.Create;
Corners2 := TAVSField.Create;
GET_CORNER_DOTS(FDose1, Corners1);
GET_CORNER_DOTS(FDose2, Corners2);
//DOTXFM(Corners, Xfm, Corners);

xmin := math.max(Corners1.Min_Coord[0],Corners2.Min_Coord[0]);
ymin := math.max(Corners1.Min_Coord[1],Corners2.Min_Coord[1]);
zmin := math.max(Corners1.Min_Coord[2],Corners2.Min_Coord[2]);
xmax := math.min(Corners1.Max_Coord[0],Corners2.Max_Coord[0]);
ymax := math.min(Corners1.Max_Coord[1],Corners2.Max_Coord[1]);
zmax := math.min(Corners1.Max_Coord[2],Corners2.Max_Coord[2]);

xnbins:=Round((xmax-xmin) / 0.2);
ynbins:=Round((ymax-ymin) / 0.2);
znbins:=Round((zmax-zmin) / 0.2);
FIELD_GRID(tmpGrid,
        xnbins,
        ynbins,
        znbins,
        xnbins*0.2,
        ynbins*0.2,
        znbins*0.2,
        xmin + ((xmax-xmin)/2),
        ymin + ((ymax-ymin)/2),
        zmin + ((zmax-zmin)/2));

FIELDXFM(FDose2, nil, tmpGrid, Gamma2, 0, 0,FIELDXFM_3Dfield, 1);
FIELDXFM(FDose1, nil, tmpGrid, Gamma1, 0, 0,FIELDXFM_3Dfield, 1);

if MaxC <> 0.0 then
begin
FIELD_MAXC(Gamma1, Gamma1, 0.001);
FIELD_MAXC(Gamma2, Gamma2, 0.001);
end;
DOSE_GAMMA(Gamma1, Gamma2, FGamma, 0.0, 0.3, 10000.0, 1.0,
StrToFloatDef(edtCriteria.Text,3.0) / 100.0, StrToFloatDef(edtDTA.Text,3.0) / 10.0,
MaxDist, Outside, NormDose, Accuracy);
FIELD_MULC(FGamma, FGamma, 100);
level := FDose1.Maximum * StrToFloatDef(edtIsodose.Text,50)/100.0;

// 2 stats mask: gamma values only in isodose% of dose1,2
FldTmp1 := TAVSField.Create;
FldTmp2 := TAVSField.Create;
try
if FDose1.Ndim=2 then
    FIELDXFM(FDose1, nil, FGamma, FldTmp1)
else
    FIELDXFM(FDose1, nil, FGamma, FldTmp1, 0, 0, FIELDXFM_3Dfield, 1);
FIELD_GTEC(FldTmp1, FldTmp1, level);
FIELD_DIVC(FldTmp1, FldTmp1, 255);
if FDose1.Ndim=2 then
    FIELDXFM(FDose2, nil, FGamma, FldTmp2)
else
    FIELDXFM(FDose2, nil, FGamma, FldTmp2, 0, 0,FIELDXFM_3Dfield, 1);
FIELD_GTEC(FldTmp2, FldTmp2, level);
FIELD_DIVC(FldTmp2, FldTmp2, 255);
// union of both volumes
//   FIELD_ADD(FldTmp1, FldTmp2, GammaStatsMask);
FIELD_COPY(FldTmp1, GammaStatsMask);
FIELD_GTEC(GammaStatsMask, GammaStatsMask, 1);
FIELD_DIVC(GammaStatsMask, GammaStatsMask, 255);
// use then GammaStatsMask for statistics
FIELD_TO_BYTE(GammaStatsMask, GammaStatsMask, 1, 1, true);
if GammaStatsMask.Datatype = AVS_TYPE_BYTE then
begin
    FIELD_MASK(FGamma, GammaStatsMask, GammaStatsMaskTmp, 0.0);
end
else
begin
    FIELD_MUL(FGamma, GammaStatsMask, GammaStatsMaskTmp);
end;

## test program

paturl = r"Z:\brent\pinnacle_dump_2\20402067"
PatientProps=TAVSField()
tmpUrl = ""
param = ""
dum = ""

#int READ_PINNACLE_compute(AVSfield** ppOut,char* pszDirectoryName,
                      #char* pszSelection, char* pszParamName, char* pszResult,
                      #char* pszExtra)
pin = READ_PINNACLE(PatientProps, paturl, tmpUrl, param , dum)

print (pin)
print (PatientProps)
print (tmpUrl)
print (param)
print (dum)



"""
    WriteProperties(subdir,FScanUrl);
    WriteProperties(subdir,FPlanUrl);
    WriteProperties(subdir,FTrialUrl);
    WriteProperties(subdir,FBeamUrl);
    WriteProperties(subdir,FDoseUrl);
    => [pinnacle local]:20402067:Patient_00000.patient\ImageSet_2.scan\_2.plan\Hersnn.trialname\1.beam\093.dose
