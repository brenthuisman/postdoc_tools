import glob,subprocess
from os import path
from shutil import copyfile
import image

dosiaengine = r"D:\postdoc\code\DosiaEngine\x64\Release\DosiaEngine.exe"
xdr_arithm = r"D:\postdoc\code\xdr_arithm\src\Win32\Debug\xdr_arithm.exe"
dosecompare = r"D:\postdoc\code\DoseCompareCmdline\src\Win32\Debug\dosecompare_cmd.exe"
xdr_cropas = r"D:\postdoc\code\xdr_cropas\src\Win32\Debug\xdr_cropas.exe"
xdr_setongrid = r"D:\postdoc\code\xdr_setongrid\src\Win32\Debug\xdr_setongrid.exe"

def execute(exe_path,args):
	assert path.isfile(exe_path)
	return subprocess.check_call( exe_path+' '+args , cwd=path.dirname(exe_path) )

def execute_getoutput(exe_path,args):
	assert path.isfile(exe_path)
	return subprocess.check_output( exe_path+' '+args , cwd=path.dirname(exe_path) )

def makedose(casedir,recalcdose=True,sumdoses=True):
	beamdirs = [path.split(i)[0] for i in glob.glob(path.join(casedir,"**","dbtype.dump"), recursive=True)]

	print("recalcdose","=",recalcdose)
	print("beamdirs","=",beamdirs)

	if recalcdose or not path.isfile(path.join(beamdirs[0],"gpumcd_dose.xdr")):
		for beamdir in beamdirs:
			arrgs = "-i "+beamdir
			execute(dosiaengine,arrgs)

	def arithm_tps(in1,in2,out):
		return '/operation add /dose1 "'+path.join(in1,'dose.xdr')+'" /dose2 "'+path.join(in2,'dose.xdr')+'" /outdose "'+out+'"'
	def arithm_gpumcd(in1,in2,out):
		return '/operation add /dose1 "'+path.join(in1,'gpumcd_dose.xdr')+'" /dose2 "'+path.join(in2,'gpumcd_dose.xdr')+'" /outdose "'+out+'"'

	tpsdosesum = path.join(casedir,'sum_dose.xdr')
	gpumcddosesum = path.join(casedir,'sum_gpumcd_dose.xdr')

	#copy mask if exists.
	# if path.isfile(path.join(beamdirs[0],'ptv.xdr')):
	# 	copyfile(path.join(beamdirs[0],'ptv.xdr'), path.join(casedir,'ptv.xdr'))

	#copy doses if only 1 beam
	if len(beamdirs) == 1:
		copyfile(path.join(beamdirs[0],'dose.xdr'),tpsdosesum)
		copyfile(path.join(beamdirs[0],'gpumcd_dose.xdr'),gpumcddosesum)
		return  [tpsdosesum,gpumcddosesum,beamdirs]

	if sumdoses:
		for i,beamdir in enumerate(beamdirs):
			args_tps=''
			args_gpumcd=''

			if (not path.isfile(tpsdosesum) and not path.isfile(gpumcddosesum)) or recalcdose:
				if i == 0:
					continue
				if i == 1:
					args_tps = arithm_tps(beamdirs[i-1],beamdirs[i],tpsdosesum)
					args_gpumcd = arithm_gpumcd(beamdirs[i-1],beamdirs[i],gpumcddosesum)

				execute(xdr_arithm,args_tps)
				execute(xdr_arithm,args_gpumcd)

	return [tpsdosesum,gpumcddosesum,beamdirs]

def comparedose(casedir,*args,**kwargs):
	dose1=''
	dose2=''
	if len(args)==0:
		#assume casedir is a dosia dumpdir
		assert path.isdir(casedir)
		dose1 = path.join(casedir,'sum_dose.xdr')
		dose2 = path.join(casedir,'sum_gpumcd_dose.xdr')
	else:
		#assume casedir is a file and secondfile also
		assert path.isfile(casedir)
		dose1 = casedir
		dose2 = args[0]#secondfile

	assert path.isfile(dose1)
	assert path.isfile(dose2)

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
		assert path.isdir(casedir)
		dose1 = path.join(casedir,'sum_dose.xdr')
		dose2 = path.join(casedir,'sum_gpumcd_dose.xdr')
	else:
		#assume casedir is a file and secondfile also
		assert path.isfile(casedir)
		dose1 = casedir
		dose2 = args[0]#secondfile

	assert path.isfile(dose1)
	assert path.isfile(dose2)

	plandose=image.image(dose1)
	otherdose=image.image(dose2)

	maskim = None
	#is there a mask?
	if path.isfile(path.join(casedir,'ptv.xdr')):
		maskim = image.image(path.abspath(path.join(casedir,'ptv.xdr')))
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

def setongrid(infile,asfile,overwrite=False):
	assert path.isfile(infile)
	assert path.isfile(asfile)
	outfile = infile+'.setongrid.xdr'

	if not path.isfile(outfile) or overwrite:
		arrgs = "/in "+infile+" /as "+asfile+" /out "+outfile+" 2>&1"
		execute(xdr_setongrid,arrgs)
		print(outfile)

	return outfile

def factor(infile,operation,factor,overwrite=False):
	outfile = infile[:-4]+".factor.xdr"

	if not path.isfile(outfile) or overwrite:
		arrgs =  '/dose1 "'+infile+'" /operation '+operation+' /factor '+factor+' /outdose "'+outfile+'"'
		execute(xdr_arithm,arrgs)

	return outfile