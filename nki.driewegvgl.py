from dataclasses import dataclass
from os import path
from nki import runners,plots
import argparse,pandas as pd
import datetime,glob

parser = argparse.ArgumentParser(description='secret')
# parser.add_argument('casedir')
parser.add_argument('--studyname',default="")
parser.add_argument('--noupdate',action='store_true') #currently does not regeneate setongrids or doses
args = parser.parse_args()

# sp = r"Z:\brent\stijn\pindump_withoverrides"
sp = r"Z:\brent\stijn\pindump_nooverrides"
sd = r"Z:\brent\stijn\dicom"
plotoutput = r"Z:\brent\stijn"
fname="6case_gammaresults"+args.studyname+datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")

# ZZIMRTe : F180307A
# ZZIMRTt : F180307B
# ZZIMRTd : F180307C
# ZZVMATe : F180307D
# ZZVMATt : F180307E
# ZZVMATd : F180307F

fname = path.join(plotoutput,fname)

if not args.noupdate:

	@dataclass
	class Case:
	    dicom_pin: str
	    dicom_mon: str
	    dosia_pin: str
	    dosia_gpumcd: str

	def mkcase(c1,c2,c3,c4):
		return Case(
			path.join(sd,c1),
			path.join(sd,c2),
			path.join(sp,c3,"sum_dose.xdr"),
			path.join(sp,c4,"sum_gpumcd_dose.xdr")
			)

	cases = [
		mkcase("imrtapin.xdr","imrtamon.xdr","F180307A","F180307A"),
		mkcase("imrtbpin.xdr","imrtbmon.xdr","F180307B","F180307B"),
		mkcase("imrtcpin.xdr","imrtcmon.xdr","F180307C","F180307C"),
		mkcase("vmatapin.xdr","vmatamon.xdr","F180307D","F180307D"),
		mkcase("vmatbpin.xdr","vmatbmon.xdr","F180307E","F180307E"),
		mkcase("vmatcpin.xdr","vmatcmon.xdr","F180307F","F180307F")
		]

	results = []

	for i,case in enumerate(cases):
		# if i == 2:
		# 	continue
		# if i == 3:
		# 	continue
		# if i == 5:
		# 	continue
		case.dicom_pin = runners.setongrid(case.dicom_pin,case.dosia_pin,)
		case.dicom_mon = runners.setongrid(case.dicom_mon,case.dosia_pin)
		case.dosia_pin = runners.factor(case.dosia_pin,'divc','100')#,True)
		case.dosia_gpumcd = runners.factor(case.dosia_gpumcd,'divc','100')#,True)

		results.append( "Studyset=PinPin "+runners.comparedose(case.dicom_pin,case.dosia_pin,files=True) )
		results.append( "Studyset=Dicom "+runners.comparedose(case.dicom_pin,case.dicom_mon,files=True) )
		results.append( "Studyset=MonDosia "+runners.comparedose(case.dosia_gpumcd,case.dicom_mon,files=True) )
		results.append( "Studyset=Dosia "+runners.comparedose(case.dosia_pin,case.dosia_gpumcd,files=True) )

	df = plots.gamma2dataframe(results,["Studyset","Files","Mean γ","γ passrate","γ99","γ95","Max γ","Min γ"])
	df.to_csv(fname+".csv")
else:
	last_fname = sorted( glob.glob(path.splitext(fname)[0].rstrip('1234567890_')+'*.csv') ,reverse=True)[0]
	df = pd.read_csv(last_fname+".csv",index_col=0)

plots.boxplot_gamma(df,fname)