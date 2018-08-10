import sys,os,glob,argparse
from nki import paths,runners,plots
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('casedir')
parser.add_argument('--recalcdose',action='store_true')
opt = parser.parse_args()

fname = os.path.join(opt.casedir,"gammaresults")+datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")

runners.makedose(opt.casedir,opt.recalcdose)
res = "Studyset="+opt.casedir+" "+runners.comparedose(opt.casedir)

df = plots.gamma2dataframe([res],["Studyset","Files","Mean γ","γ passrate","γ99","γ95","Max γ","Min γ"]) #distributions dont make sense for one case, but OK
df.to_csv(fname+".csv")

plots.boxplot_gamma(df,fname)