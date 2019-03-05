import sys,os,glob,argparse,subprocess, pandas as pd
from shutil import copyfile
import datetime
from nki import runners,plots
import image
from pathlib import Path

parser = argparse.ArgumentParser(description='secret')
parser.add_argument('pindumpdir')
parser.add_argument('--recalcdose',action='store_true')
# parser.add_argument('--nosum',action='store_true')
args = parser.parse_args()

pindumpdir = args.pindumpdir
recalcdose = args.recalcdose
fname = os.path.join(args.pindumpdir,"gammaresults")+datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")

res=[]
dvhres=[]
cases = [x for x in glob.glob(os.path.join(pindumpdir,"*/"), recursive=False) if not os.path.dirname(x).split(os.sep)[-1].startswith('__')]

if True: #recalcdose
	for casedir in cases:
		patient=runners.dir2plans(casedir)
		for key,plan in patient.items():
			try:
				gpubeamdoses = []
				pinbeamdoses = []
				for i,beam in enumerate(plan):
					runners.calcdose(beam,recalcdose)
					gpubeamdoses.append(image.image(beam/"gpumcd_dose.xdr"))
					pinbeamdoses.append(image.image(beam/"dose.xdr"))
					mask=beam/"ptvmask.xdr"
					if i==0 and mask.is_file():
						copyfile(mask, key+"ptvmask.xdr")

				##sommen
				if len(gpubeamdoses)>1:
					for i in range(1,len(gpubeamdoses)):
						gpubeamdoses[0].add(gpubeamdoses[i])
						pinbeamdoses[0].add(pinbeamdoses[i])
				gpubeamdoses[0].saveas(key+"sumpin.xdr")
				pinbeamdoses[0].saveas(key+"sumgpu.xdr")

			except subprocess.CalledProcessError:
				print("Dose generation for case",casedir,"failed to execute, skipped for analysis.")
				continue #can skip what follows.

			try:
				res.append("Studyset="+key+" "+runners.calcgamma(Path(key+"sumpin.xdr"),Path(key+"sumgpu.xdr"),Path(key+'gammamap.xdr'),Path(key+"ptvmask.xdr"),recalcdose))
				dvhres.append("Studyset="+key+" "+runners.calcdvh(Path(key+"sumpin.xdr"),Path(key+"sumgpu.xdr"),Path(key+"ptvmask.xdr")))
			except (subprocess.CalledProcessError,AssertionError):
				print("Dose comparison for case",plan,"failed to execute, skipped for analysis.")
	df = plots.gamma2dataframe(res)#,["Studyset","Files","Mean γ","γ passrate","γ99","γ95","Max γ","Min γ"])
	df.to_csv(fname+".gamma.csv")
	dfdvh = plots.gamma2dataframe(dvhres)
	dfdvh.to_csv(fname+".dvh.csv")
else:
	last_fname = sorted( glob.glob(os.path.splitext(fname)[0].rstrip('1234567890_')+'*.gamma.csv') ,reverse=True)[0]
	df = pd.read_csv(last_fname,index_col=0)

	last_fnamedvh = sorted( glob.glob(os.path.splitext(fname)[0].rstrip('1234567890_')+'*.dvh.csv') ,reverse=True)[0]
	dfdvh = pd.read_csv(last_fnamedvh,index_col=0)

plots.boxplot_gamma(df,fname+'gamma', studyset_split=False)
plots.boxplot_gamma(df,fname+'gamma')

plots.boxplot_gamma(dfdvh,fname+'dvh', studyset_split=False)
plots.boxplot_gamma(dfdvh,fname+'dvh')
