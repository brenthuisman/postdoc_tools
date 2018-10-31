#!/usr/bin/env python3

#sysimports
import argparse
from os import path
#package imports
import seaborn as sns,pandas as pd
#local imports
import image,plot
from nki import plots
# from nki import runners

fname = path.join(r"Z:\brent\fieldseries\F180813B",'profile_plot')
df = pd.read_csv(fname+".csv",index_col=0)
fname_shift = path.join(r"Z:\brent\fieldseries\F180823Q",'profile_plot')
df_shift = pd.read_csv(fname_shift+".csv",index_col=0)

columntitles = ["Plan","Axis","Fieldsize","Penumbra"]

data = []
for dataset,penum_links,penum_rechts in plots.get_penumbras(df.query("Axis=='X' and (Setname=='5cm' or Setname=='10cm' or Setname=='15cm' or Setname=='20cm')")):
    # data.append(["isocentred","x",dataset,penum_links,penum_rechts])
    data.append(["isocentred","X (BLD:Jaw)",dataset,penum_links])
    data.append(["isocentred","X (BLD:Jaw)",dataset,penum_rechts])
    # print("Penumbra's voor ",dataset,penum_links,penum_rechts)
for dataset,penum_links,penum_rechts in plots.get_penumbras(df.query("Axis=='Z' and (Setname=='5cm' or Setname=='10cm' or Setname=='15cm' or Setname=='20cm')")):
    data.append(["isocentred","Z (BLD:MLC)",dataset,penum_links])
    data.append(["isocentred","Z (BLD:MLC)",dataset,penum_rechts])
    # print("Penumbra's voor ",dataset,penum_links,penum_rechts)
for dataset,penum_links,penum_rechts in plots.get_penumbras(df_shift.query("Axis=='X' and (Setname=='5cm' or Setname=='10cm' or Setname=='15cm' or Setname=='20cm')")):
    data.append(["shifted","X (BLD:Jaw)",dataset,penum_links])
    data.append(["shifted","X (BLD:Jaw)",dataset,penum_rechts])
    # print("Penumbra's voor ",dataset,penum_links,penum_rechts)
for dataset,penum_links,penum_rechts in plots.get_penumbras(df_shift.query("Axis=='Z' and (Setname=='5cm' or Setname=='10cm' or Setname=='15cm' or Setname=='20cm')")):
    data.append(["shifted","Z (BLD:MLC)",dataset,penum_links])
    data.append(["shifted","Z (BLD:MLC)",dataset,penum_rechts])
    # print("Penumbra's voor ",dataset,penum_links,penum_rechts)

newdf = pd.DataFrame(data = data,columns = columntitles)

sns.set_style(style="whitegrid")

f = sns.catplot(x="Fieldsize", y="Penumbra", hue="Plan", data=newdf, col="Axis", kind="box", sharey=True)
f.savefig(r'Z:\brent\fieldseries\penumbra.pdf', bbox_inches='tight')
f.savefig(r'Z:\brent\fieldseries\penumbra.png', bbox_inches='tight',dpi=300)
