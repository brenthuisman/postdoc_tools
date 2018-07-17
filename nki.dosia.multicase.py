import sys,os,glob,argparse
from nki import paths,runners,plots

parser = argparse.ArgumentParser(description='secret')
parser.add_argument('pindumpdir')
parser.add_argument('--update',action='store_true')
args = parser.parse_args()

pindumpdir = args.pindumpdir
update = args.update
fname = args.pindumpdir+"gammaresults"

res=[]
cases = [x for x in glob.glob(os.path.join(pindumpdir,"*/")) if not os.path.dirname(x).split(os.sep)[-1].startswith('__')]

for casedir in cases:
	try:
		runners.makedose(casedir,update)
		res.append(runners.comparedose(casedir))
	except AssertionError as e:
		print ("================= Holy Shit! ==================")
		print (e)
		print (casedir)
		print ("================= ========== ==================")


df = plots.gamma2dataframe(res)
df.to_csv(fname+".csv")

plots.boxplot_gamma(df,fname)