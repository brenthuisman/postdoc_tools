from dataclasses import dataclass
from os import path
from nki import runners,plots
import argparse,pandas as pd

parser = argparse.ArgumentParser(description='secret')
# parser.add_argument('pindumpdir')
parser.add_argument('--update',action='store_true') #currently does not regeneate setongrids or doses
args = parser.parse_args()

# sp = r"Z:\brent\stijn\pindump_noiav"
sp = r"Z:\brent\stijn\pindump"
sd = r"Z:\brent\stijn\dicom"
plotoutput = r"Z:\brent\stijn"
fname="gammaresults"

# ZZIMRTe : F180307A
# ZZIMRTt : F180307B
# ZZIMRTd : F180307C
# ZZVMATe : F180307D
# ZZVMATt : F180307E
# ZZVMATd : F180307F

fname = path.join(plotoutput,fname)

if not path.isfile(fname+".csv") or args.update:

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

	# results_pinpin = []
	# results_dicom = []
	# results_mondosia = []
	# results_dosia = []

	for i,case in enumerate(cases):
		if i == 2:
			continue
		if i == 3:
			continue
		if i == 5:
			continue
		case.dicom_pin = runners.setongrid(case.dicom_pin,case.dosia_pin)
		case.dicom_mon = runners.setongrid(case.dicom_mon,case.dosia_pin)
		case.dosia_pin = runners.factor(case.dosia_pin,'divc','100')
		case.dosia_gpumcd = runners.factor(case.dosia_gpumcd,'divc','100')

		# results_pinpin.append( runners.comparedose(case.dicom_pin,case.dosia_pin) )
		# results_dicom.append( runners.comparedose(case.dicom_pin,case.dicom_mon) )
		# results_mondosia.append( runners.comparedose(case.dosia_gpumcd,case.dicom_mon) )
		# results_dosia.append( runners.comparedose(case.dosia_pin,case.dosia_gpumcd) )

		results.append( "Studyset=PinPin "+runners.comparedose(case.dicom_pin,case.dosia_pin,files=True) )
		results.append( "Studyset=Dicom "+runners.comparedose(case.dicom_pin,case.dicom_mon,files=True) )
		results.append( "Studyset=MonDosia "+runners.comparedose(case.dosia_gpumcd,case.dicom_mon,files=True) )
		results.append( "Studyset=Dosia "+runners.comparedose(case.dosia_pin,case.dosia_gpumcd,files=True) )

	# ex output: Mean=0.01 ppc<1=100.00 p99=0.15 p95=0.07 Max=0.43 Min=0.00
	columns = ["Studieset","Files","Mean γ","γ passrate","γ99","γ95","Max γ","Min γ"]
	# columns = ["Studieset","Mean G","G passrate","G99","G95","Max dose","Min dose"]
	data = []
	for line in results:
		row=[]
		for item in line.split():
			try:
				row.append(float(item.split('=')[-1]))
			except ValueError:
				row.append(item.split('=')[-1])
		data.append(row)

	df = pd.DataFrame(data = data,columns = columns)
	df.to_csv(fname+".csv")

df = pd.read_csv(fname+".csv",index_col=0)

# print(df)

plots.boxplot_gamma(df,fname)
# plots.boxplot_gamma(results_pinpin,path.join(plotoutput,"results_pinpin"))
# plots.boxplot_gamma(results_dicom,path.join(plotoutput,"results_dicom"))
# plots.boxplot_gamma(results_mondosia,path.join(plotoutput,"results_mondosia"))
# plots.boxplot_gamma(results_dosia,path.join(plotoutput,"results_dosia"))
