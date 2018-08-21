import sys,os,glob,argparse
from nki import paths,runners,plots
import datetime

parser = argparse.ArgumentParser(description='secret')
parser.add_argument('pindumpdir')
parser.add_argument('--recalcdose',action='store_true')
parser.add_argument('--nosum',action='store_true')
args = parser.parse_args()

pindumpdir = args.pindumpdir
recalcdose = args.recalcdose
fname = os.path.join(args.pindumpdir,"gammaresults")+datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")

res=[]
cases = [x for x in glob.glob(os.path.join(pindumpdir,"*/"), recursive=True) if not os.path.dirname(x).split(os.sep)[-1].startswith('__')]

for casedir in cases:
	try:
		runners.makedose(casedir,recalcdose,not args.nosum)
		if not args.nosum:
			res.append("Studyset="+casedir+" "+runners.comparedose(casedir))
	except AssertionError as e:
		print ("================= Holy Shit! ==================")
		print (e)
		print (casedir)
		print ("================= ========== ==================")


df = plots.gamma2dataframe(res,["Studyset","Files","Mean γ","γ passrate","γ99","γ95","Max γ","Min γ"])
df.to_csv(fname+".csv")

plots.boxplot_gamma(df,fname)