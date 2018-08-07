import sys,os,glob,argparse
from nki import paths,runners,plots
import datetime

parser = argparse.ArgumentParser(description='secret')
parser.add_argument('casedir')
parser.add_argument('--recalcdose',action='store_true')
args = parser.parse_args()

casedir = args.casedir
recalcdose = args.recalcdose
fname = os.path.join(args.casedir,"gammaresults")+datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")

runners.makedose(casedir,recalcdose)
res = "Studyset="+casedir+" "+runners.comparedose(casedir)

df = plots.gamma2dataframe([res],["Studyset","Files","Mean γ","γ passrate","γ99","γ95","Max γ","Min γ"]) #distributions dont make sense for one case, but OK
df.to_csv(fname+".csv")

plots.boxplot_gamma(df,fname)