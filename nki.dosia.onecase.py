import sys,os,glob,argparse
from nki import paths,runners,plots

parser = argparse.ArgumentParser(description='secret')
parser.add_argument('casedir')
parser.add_argument('--update',action='store_true')
args = parser.parse_args()

casedir = args.casedir
update = args.update
fname = args.casedir+"gammaresults"

runners.makedose(casedir,update)
res = runners.comparedose(casedir)

df = plots.gamma2dataframe([res]) #distributions dont make sense for one case, but OK
df.to_csv(fname+".csv")

plots.boxplot_gamma(df,fname)