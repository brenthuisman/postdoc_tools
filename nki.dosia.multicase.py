import sys,os,glob,argparse
from nki import paths,runners,plots

parser = argparse.ArgumentParser(description='secret')
parser.add_argument('pindumpdir')
parser.add_argument('--update',action='store_true')
args = parser.parse_args()

pindumpdir = args.pindumpdir
update = args.update

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

plots.boxplot_gamma(res,os.path.join(pindumpdir,'gammaresults'))

with open(os.path.join(pindumpdir,'gammaresults.txt'),'w') as resultfile:
	resultfile.writelines([i+': '+j for i,j in zip(cases,res)])
