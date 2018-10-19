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

# f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
# sns.boxplot(x="Fieldsize", y="Penumbra", hue="Plan", data=newdf, ax=ax1, lw=1)

f = sns.catplot(x="Fieldsize", y="Penumbra", hue="Plan", data=newdf, col="Axis", kind="box", sharey=True)
# f.set_axis_labels("", "Difference")
# f, ax = plt.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
# ax = sns.boxplot(y="value", x="variable", data=df)

f.savefig(r'Z:\brent\fieldseries\penumbra.pdf', bbox_inches='tight')
f.savefig(r'Z:\brent\fieldseries\penumbra.png', bbox_inches='tight',dpi=300)

# ax1.set_xlim(-70,70)
# # ax2.set_xlim(-70,70)
# ax3.set_xlim(-70,70)
# ax4.set_xlim(-70,70)

# # ax3.set_ylim(-.25,0.5)
# ax3.set_ylim(0,2)

# ax1.set_title("X (BLD:Jaw)")
# ax2.set_title("Y")
# # ax3.set_title("reldiff X") #relY is relative y over X axis
# ax3.set_title("ratio X") #relY is relative y over X axis
# ax4.set_title("Z (BLD:MLC)")

# # ax3.set_ylabel("Relative Dose")
# # ax3.set_ylabel("Dose Ratio")

# ax1.legend(title="Fieldsize", loc='upper right', bbox_to_anchor=(1.4, 1.),frameon=False)
# ax2.legend_.remove()#.legend().set_title('Fieldsize')
# ax3.legend(title="Relative to Pinnacle", loc='upper right', bbox_to_anchor=(1.4, 1.),frameon=False)
# ax4.legend_.remove()#.legend().set_title('Fieldsize')

# f.subplots_adjust(hspace=.6,wspace=.5)
# f.savefig(fname+'.pdf', bbox_inches='tight')
# f.savefig(fname+'.png', bbox_inches='tight',dpi=300)