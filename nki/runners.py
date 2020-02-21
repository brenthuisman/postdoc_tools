import subprocess,collections
from pathlib import Path
from medimage import image

dosiaengine = r"D:\postdoc\code\DosiaEngine\x64\Release\DosiaEngine.exe"
xdr_gamma = r"D:\postdoc\code\xdr_gamma\src\Win32\Debug\xdr_gamma.exe"

#old:
dosecompare = r"D:\postdoc\code\DoseCompareCmdline\src\Win32\Debug\dosecompare_cmd.exe"
xdr_cropas = r"D:\postdoc\code\xdr_cropas\src\Win32\Debug\xdr_cropas.exe"
xdr_arithm = r"D:\postdoc\code\xdr_arithm\src\Win32\Debug\xdr_arithm.exe"
xdr_setongrid = r"D:\postdoc\code\xdr_setongrid\src\Win32\Debug\xdr_setongrid.exe"

def execute(exe_path,args):
	exe_path = Path(exe_path)
	assert exe_path.is_file()
	return subprocess.check_call( str(exe_path)+' '+args , cwd=exe_path.parent )

def execute_getoutput(exe_path,args):
	exe_path = Path(exe_path)
	assert exe_path.is_file()
	return subprocess.check_output( str(exe_path)+' '+args , cwd=exe_path.parent )


def dir2plans(indir):
	'''
	generate a list of lists of cases. each case consist of a number of beamdirs.
	pat.>plan>beams
	'''
	beamdirs = [i.parent for i in Path(indir).glob("**/dbtype.dump")]

	patientdict=collections.defaultdict(list) #init vals with empty list
	for beamdir in beamdirs:
		key=str(beamdir)[:-7] #key
		patientdict[key].append(beamdir)
	return patientdict

def calcdose(beamdir,overwrite=True):
	if not overwrite and (beamdir/"gpumcd_dose.xdr").is_file():
		return
	arrgs = "-i "+str(beamdir)
	execute(dosiaengine,arrgs)
	return


def calcgamma(dose1,dose2,outf,mask=None,overwrite=True):
	if overwrite:
		arrgs = "/dose1 "+str(dose1)+" /dose2 "+str(dose2)+" /outf "+str(outf)+" 2>&1"
		print(arrgs)
		execute(xdr_gamma,arrgs)
	gammamap = image(outf)
	if mask == None or not mask.is_file():
		print('No mask or maskregion specified; using isodose 50 volume of gammamap for gamma statistical analysis.')
		maskim = image(dose1)
		maskim.tomask_atthreshold((50/100.)*maskim.max())
	else:
		maskim = image(mask)
	gammamap.applymask(maskim)
	result = 'mean='+str(gammamap.mean())+' passrate='+str(gammamap.passrate())
	result = "files="+str(dose1)+";"+str(dose2)+" "+result

	gammamap.saveas(str(outf)+'.masked.xdr')
	return result


def calcdvh(dose1,dose2,mask=None):
	plandose=image(dose1)
	otherdose=image(dose2)
	if mask == None or not mask.is_file():
		print('No mask or maskregion specified; using isodose 50 volume of plandose for DVH analysis.')
		maskim = plandose.copy()
		maskim.tomask_atthreshold((50/100.)*maskim.max())
	else:
		maskim = image(mask)

	plandose.applymask(maskim)
	otherdose.applymask(maskim)

	# note: array is sorted in reverse for DVHs, i.e. compute 100-n%
	planD2,planD50,planD98 = plandose.percentiles([98,50,2])
	otherD2,otherD50,otherD98 = otherdose.percentiles([98,50,2])

	labels = ["Dmax","D2","D50","D98","Dmean"]
	planres = plandose.max(),planD2,planD50,planD98,plandose.mean()
	otherres = otherdose.max(),otherD2,otherD50,otherD98,otherdose.mean()
	diffres = [label+"="+str(i-j) for label,i,j in zip(labels,planres,otherres)]

	print(diffres)

	result = "files="+str(dose1)+";"+str(dose2)+" "+' '.join(diffres)

	return result


def makedose_old(casedir,recalcdose=True,sumdoses=True):
	import glob,os
	from shutil import copyfile
	beamdirs = [os.path.split(i)[0] for i in glob.glob(os.path.join(casedir,"**","dbtype.dump"), recursive=True)]

	print("recalcdose","=",recalcdose)
	print("beamdirs","=",beamdirs)

	if recalcdose or not os.path.isfile(os.path.join(beamdirs[0],"gpumcd_dose.xdr")):
		for beamdir in beamdirs:
			arrgs = "-i "+beamdir
			execute(dosiaengine,arrgs)

	#copy mask if exists.
	if os.path.isfile(os.path.join(beamdirs[0],'ptvmask.xdr')):
		copyfile(os.path.join(beamdirs[0],'ptvmask.xdr'), os.path.join(casedir,'ptvmask.xdr'))

	tpsdosesum_fn = os.path.join(casedir,'sum_dose.xdr')
	gpumcddosesum_fn = os.path.join(casedir,'sum_gpumcd_dose.xdr')

	tpsdosesum = image(os.path.join(beamdirs[0],'dose.xdr'))
	gpumcddosesum = image(os.path.join(beamdirs[0],'gpumcd_dose.xdr'))

	if len(beamdirs) > 1:
		for beamdir in beamdirs[1:]:
			print(os.path.join(beamdir,'dose.xdr'))
			imaget = image(os.path.join(beamdir,'dose.xdr'))
			imageg = image(os.path.join(beamdir,'gpumcd_dose.xdr'))
			tpsdosesum.add(imaget)
			gpumcddosesum.add(imageg)

	tpsdosesum.saveas(tpsdosesum_fn)
	gpumcddosesum.saveas(gpumcddosesum_fn)

	return [tpsdosesum_fn,gpumcddosesum_fn,beamdirs]

def comparedose_old(casedir,*args,**kwargs):
	import os
	dose1=''
	dose2=''
	if len(args)==0:
		#assume casedir is a dosia dumpdir
		assert os.path.isdir(casedir)
		dose1 = os.path.join(casedir,'sum_dose.xdr')
		dose2 = os.path.join(casedir,'sum_gpumcd_dose.xdr')
	else:
		#assume casedir is a file and secondfile also
		assert os.path.isfile(casedir)
		dose1 = casedir
		dose2 = args[0]#secondfile

	assert os.path.isfile(dose1)
	assert os.path.isfile(dose2)

	arrgs = "/dose1 "+dose1+" /dose2 "+dose2+" 2>&1"
	result = execute_getoutput(dosecompare,arrgs).decode('utf-8').strip()
	print(result)

	result = "files="+dose1+";"+dose2+" "+result

	return result

def dvhcompare(casedir,*args,**kwargs):
	dose1=''
	dose2=''
	if len(args)==0:
		#assume casedir is a dosia dumpdir
		assert os.path.isdir(casedir)
		dose1 = os.path.join(casedir,'sum_dose.xdr')
		dose2 = os.path.join(casedir,'sum_gpumcd_dose.xdr')
	else:
		#assume casedir is a file and secondfile also
		assert os.path.isfile(casedir)
		dose1 = casedir
		dose2 = args[0]#secondfile

	assert os.path.isfile(dose1)
	assert os.path.isfile(dose2)

	plandose=image(dose1)
	otherdose=image(dose2)

	maskim = None
	#is there a mask?
	if os.path.isfile(os.path.join(casedir,'ptv.xdr')):
		maskim = image(os.path.absos.path(os.path.join(casedir,'ptv.xdr')))
	else:
		print('No mask or maskregion specified; using isodose 50 volume of plandose for DVH analysis.')
		maskim = plandose.copy()
		maskim.tomask_atthreshold((50/100.)*maskim.max())

	plandose.applymask(maskim)
	otherdose.applymask(maskim)

	# note: array is sorted in reverse for DVHs, i.e. compute 100-n%
	planD2,planD50,planD98 = plandose.percentiles([98,50,2])
	otherD2,otherD50,otherD98 = otherdose.percentiles([98,50,2])

	labels = ["Dmax","D2","D50","D98","Dmean"]
	planres = plandose.max(),planD2,planD50,planD98,plandose.mean()
	otherres = otherdose.max(),otherD2,otherD50,otherD98,otherdose.mean()
	diffres = [label+"="+str(i-j) for label,i,j in zip(labels,planres,otherres)]

	print(diffres)

	result = "files="+dose1+";"+dose2+" "+' '.join(diffres)

	return result

def setongrid_old(infile,asfile,overwrite=False):
	import os
	assert os.path.isfile(infile)
	assert os.path.isfile(asfile)
	outfile = infile+'.setongrid.xdr'

	if not os.path.isfile(outfile) or overwrite:
		arrgs = "/in "+infile+" /as "+asfile+" /out "+outfile+" 2>&1"
		execute(xdr_setongrid,arrgs)
		print(outfile)

	return outfile

def factor_old(infile,operation,factor,overwrite=False):
	import os
	outfile = infile[:-4]+".factor.xdr"

	if not os.path.isfile(outfile) or overwrite:
		arrgs =  '/dose1 "'+infile+'" /operation '+operation+' /factor '+factor+' /outdose "'+outfile+'"'
		execute(xdr_arithm,arrgs)

	return outfile