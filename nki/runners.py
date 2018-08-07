import glob,subprocess
from os import path
from nki import paths

def execute(exe_path,args):
	assert path.isfile(exe_path)
	return subprocess.check_call( exe_path+' '+args , cwd=path.dirname(exe_path) )

def execute_getoutput(exe_path,args):
	assert path.isfile(exe_path)
	return subprocess.check_output( exe_path+' '+args , cwd=path.dirname(exe_path) )

def makedose(casedir,recalcdose=True): #update=false is NOT COMPUTING new dose
	beamdirs = [path.split(i)[0] for i in glob.glob(path.join(casedir,"**","dbtype.dump"))]

	print("recalcdose","=",recalcdose)

	if recalcdose:
		for beamdir in beamdirs:
			arrgs = "-i "+beamdir
			execute(paths.dosiaengine,arrgs)

	def arithm_tps(in1,in2,out):
		return '/operation add /dose1 "'+path.join(in1,'dose.xdr')+'" /dose2 "'+path.join(in2,'dose.xdr')+'" /outdose "'+out+'"'
	def arithm_gpumcd(in1,in2,out):
		return '/operation add /dose1 "'+path.join(in1,'gpumcd_dose.xdr')+'" /dose2 "'+path.join(in2,'gpumcd_dose.xdr')+'" /outdose "'+out+'"'

	tpsdosesum=''
	gpumcddosesum=''

	if len(beamdirs) == 1:
		tpsdosesum = path.join(beamdirs[0],'sum_dose.xdr')
		gpumcddosesum = path.join(beamdirs[0],'sum_gpumcd_dose.xdr')
	else:
		tpsdosesum = path.join(casedir,'sum_dose.xdr')
		gpumcddosesum = path.join(casedir,'sum_gpumcd_dose.xdr')

	for i,beamdir in enumerate(beamdirs):
		args_tps=''
		args_gpumcd=''

		if (not path.isfile(tpsdosesum) and not path.isfile(gpumcddosesum)) or recalcdose:
			if i == 0:
				continue
			if i == 1:
				args_tps = arithm_tps(beamdirs[i-1],beamdirs[i],tpsdosesum)
				args_gpumcd = arithm_gpumcd(beamdirs[i-1],beamdirs[i],gpumcddosesum)

			execute(paths.xdr_arithm,args_tps)
			execute(paths.xdr_arithm,args_gpumcd)

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
	result = execute_getoutput(paths.dosecompare,arrgs).decode('utf-8').strip()
	print(result)

	result = "files="+dose1+";"+dose2+" "+result

	return result

def setongrid(infile,asfile,overwrite=False):
	assert path.isfile(infile)
	assert path.isfile(asfile)
	outfile = infile+'.setongrid.xdr'

	if not path.isfile(outfile) or overwrite:
		arrgs = "/in "+infile+" /as "+asfile+" /out "+outfile+" 2>&1"
		execute(paths.xdr_setongrid,arrgs)
		print(outfile)

	return outfile

def factor(infile,operation,factor,overwrite=False):
	outfile = infile[:-4]+".factor.xdr"

	if not path.isfile(outfile) or overwrite:
		arrgs =  '/dose1 "'+infile+'" /operation '+operation+' /factor '+factor+' /outdose "'+outfile+'"'
		execute(paths.xdr_arithm,arrgs)

	return outfile