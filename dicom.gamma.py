#pip install simpleitk scikit-image

import os,subprocess,pydicom,numpy as np,SimpleITK as sitk
from skimage import io #cant use skimage.io.$whatevs

study_dir = r"Z:\brent\DataVoorBrent"
dicom_file_monaco = r"VMATc\Monaco\F180307F_MonacoRecalc_Dose.dcm"
dicom_file_pinnacle = r"VMATc\Pinnacle\2.16.840.1.113669.2.931128.223131424.20180307145214.986059_0001_000001_1520430915045d.dcm"

test_xdr = r"Z:\brent\dosia_validatiedump\AA171214\Epid_6MV_COM.trialname.1.beam\ct.xdr"
test_mhd = r"Z:\brent\dosia_validatiedump\AA171214\Epid_6MV_COM.trialname.1.beam\dose.mhd"

print(os.path.join(study_dir,dicom_file_monaco))

mon = pydicom.read_file(os.path.join(study_dir,dicom_file_monaco),force=True)
pin = pydicom.read_file(os.path.join(study_dir,dicom_file_pinnacle))

#print(io.find_available_plugins())
#quit()

#mon_im = sitk.ReadImage(test_mhd) #no dicom, xdr
mon_im = io.imread(test_mhd,plugin='simpleitk')

lijssie = [mon,pin]

for dicomm in lijssie:
    for key in dicomm.dir():
        value = getattr(dicomm, key, '')
        #if type(value) is pydicom.UID.UID or key == "PixelData":
        if key == "PixelData":
            continue

        print("%s: %s" % (key, value))


    #d = np.fromstring(dicomm.PixelData,dtype=numpy.int16)
    #d = d.reshape((dicomm.NumberofFrames,dicomm.Columns,dicomm.Rows))

#with open(os.path.join(local_pinnacle_dir,'purls.txt'),'r') as purls:
    #for line in purls.readlines():
        #if 'Epid' in line:
            #continue
        #cmd=dosia_exe+' /beam '+line+' /outdir '+outdir
        #print( cmd )
        ##os.popen( cmd )
        #try:
            #subprocess.check_call( cmd )
        #except subprocess.CalledProcessError:
            #failed_dumps.append(line+'\n')

#with open(os.path.join(outdir,'dump_fails.txt'),'w') as failfile:
    #failfile.writelines(failed_dumps) #doesnt do newlines
