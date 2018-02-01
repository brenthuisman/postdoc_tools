## Match42 shite
import importlib.util
spec = importlib.util.spec_from_file_location("M42_Python", "D:\install\Match42\python\M42_Python.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)

from M42_Python import READ_PINNACLE, TAVSField

## general imports



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
