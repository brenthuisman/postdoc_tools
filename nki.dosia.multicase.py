import sys,os,glob,argparse,subprocess, pandas as pd
from nki import runners,plots
import datetime

parser = argparse.ArgumentParser(description='secret')
parser.add_argument('pindumpdir')
parser.add_argument('--recalcdose',action='store_true')
# parser.add_argument('--nosum',action='store_true')
args = parser.parse_args()

pindumpdir = args.pindumpdir
recalcdose = args.recalcdose
fname = os.path.join(args.pindumpdir,"gammaresults")+datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")

res=[]
# if args.nosum:
# 	cases = [pindumpdir]
# else:
cases = [x for x in glob.glob(os.path.join(pindumpdir,"*/"), recursive=True) if not os.path.dirname(x).split(os.sep)[-1].startswith('__')]

if True: #recalcdose
	for casedir in cases:
		# try:
		try:
			# runners.makedose(casedir,recalcdose,not args.nosum)
			runners.makedose(casedir,recalcdose)
		except subprocess.CalledProcessError:
			print("Dose generation for case",casedir,"failed to execute, skipped for analysis.")
		# if not args.nosum:
		try:
			res.append("Studyset="+casedir+" "+runners.comparedose(casedir))
		except (subprocess.CalledProcessError,AssertionError):
			print("Dose comparison for case",casedir,"failed to execute, skipped for analysis.")
		# except AssertionError as e:
		# 	print ("================= Holy Shit! ==================")
		# 	print (e)
		# 	print (casedir)
		# 	print ("================= ========== ==================")
	# if not args.nosum:
	df = plots.gamma2dataframe(res,["Studyset","Files","Mean γ","γ passrate","γ99","γ95","Max γ","Min γ"])
	df.to_csv(fname+".csv")
else:
	last_fname = sorted( glob.glob(os.path.splitext(fname)[0].rstrip('1234567890_')+'*.csv') ,reverse=True)[0]
	df = pd.read_csv(last_fname,index_col=0)

plots.boxplot_gamma(df,fname, studyset_split=False)
plots.boxplot_gamma(df,fname)
