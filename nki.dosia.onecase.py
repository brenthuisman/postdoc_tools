import sys,os,glob,argparse
from nki import paths,runners,plots

parser = argparse.ArgumentParser(description='secret')
parser.add_argument('casedir')
parser.add_argument('--update',action='store_true')
args = parser.parse_args()

casedir = args.casedir
update = args.update

runners.makedose(casedir,update)
res = runners.comparedose(casedir)
plots.boxplot_gamma(res,os.path.join(casedir,'gammaresult'))

## todo maak profielplot van beide.
