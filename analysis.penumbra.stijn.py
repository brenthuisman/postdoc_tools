#!/usr/bin/env python3

#sysimports
import argparse
from os import path
#package imports
import seaborn as sns,pandas as pd,numpy as np
#local imports
import image,plot
from nki import plots
# from nki import runners

parser = argparse.ArgumentParser(description='specify mulitple mhd images to analyse')
parser.add_argument('--noupdate',action='store_true')
opt = parser.parse_args()

# fname = path.join(r"Z:\brent\stijn\__results\blok\minus_stijnpin",'profile_plot')
if True:
# if not opt.noupdate:
    ## lets make csv
    imagefiles = [r"Z:\brent\stijn\pindump_nooverrides\MonacoPhantom\sum_dose.factor.mhd",
    r"Z:\brent\stijn\pindump_nooverrides\MonacoPhantom\sum_gpumcd_dose.factor.mhd",
    r"Z:\brent\stijn\dicom\blokmon.xdr.setongrid.xdr.mhd"]

    setnames = ["Pinnacle","Dosia","Monaco"]

    glob_y_x = None
    pdd_max = None
    center_x = None
    center_z = None

    listoframes=[]
    for i,setname in enumerate(setnames):
        im = image.image( imagefiles[i] )

        x_x = im.get_axis_mms('x')
        x_y = im.get_axis_mms('y')
        x_z = im.get_axis_mms('z')

        # pdd_max = im.getline('y').argmax()
        if glob_y_x is None:
            pdd_max = im.get1dlist([1,0,1]).argmax()
            center_x = im.get1dlist([1,1,0]).argmax() #x,z indices swapped!!!
            center_z = im.get1dlist([0,1,1]).argmax()

            print("midden van PDD max:",imagefiles[i],center_x,pdd_max,center_z)

        y_x = im.getline_atindex('x',pdd_max,center_z)
        y_y = im.getline_atindex('y',center_x,center_z)
        y_z = im.getline_atindex('z',center_x,pdd_max)

        if glob_y_x is not None:
            with np.errstate(divide='ignore',invalid='ignore'):
                # y_xrel = ( gy_x - py_x ) / py_x
                y_xrat = y_x / glob_y_x
                listoframes.append( plots.cols2dataframe(columntitles,x_x,y_xrat,metadata=[setname,'ratio','ratY']) )
        else:
            glob_y_x = y_x

        columntitles = ["Setname","Generator","Axis",'Distance to isoc [mm]','Dose [cGy]']
        listoframes.append( plots.cols2dataframe(columntitles,x_x,y_x,metadata=[setname,setname,'X']) )
        listoframes.append( plots.cols2dataframe(columntitles,x_y,y_y,metadata=[setname,setname,'Y']) )
        listoframes.append( plots.cols2dataframe(columntitles,x_z,y_z,metadata=[setname,setname,'Z']) )
        # listoframes.append( plots.cols2dataframe(columntitles,x_x,y_xrel,metadata=[setname,'reldiff','relY']) )

    df = pd.concat(listoframes)
    df.to_csv(r"Z:\brent\stijn\__results\blok\penumbra.csv")
    # print(df)

columntitles = ["Plan","Axis","Fieldsize","Penumbra"]

data = []
for dataset,penum_links,penum_rechts in plots.get_penumbras(df.query("Axis=='X'")):
    # data.append(["isocentred","x",dataset,penum_links,penum_rechts])
    data.append(["isocentred","X (BLD:Jaw)",dataset,penum_links])
    data.append(["isocentred","X (BLD:Jaw)",dataset,penum_rechts])
    # print("Penumbra's voor ",dataset,penum_links,penum_rechts)
for dataset,penum_links,penum_rechts in plots.get_penumbras(df.query("Axis=='Z'")):
    data.append(["isocentred","Z (BLD:MLC)",dataset,penum_links])
    data.append(["isocentred","Z (BLD:MLC)",dataset,penum_rechts])
    # print("Penumbra's voor ",dataset,penum_links,penum_rechts)

newdf = pd.DataFrame(data = data,columns = columntitles)

sns.set_style(style="whitegrid")

# f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
# sns.boxplot(x="Fieldsize", y="Penumbra", hue="Plan", data=newdf, ax=ax1, lw=1)

f = sns.catplot(x="Fieldsize", y="Penumbra", hue="Plan", data=newdf, col="Axis", kind="box", sharey=True)
# f.set_axis_labels("", "Difference")
# f, ax = plt.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
# ax = sns.boxplot(y="value", x="variable", data=df)

f.savefig(r'Z:\brent\stijn\__results\blok\penumbra.pdf', bbox_inches='tight')
f.savefig(r'Z:\brent\stijn\__results\blok\penumbra.png', bbox_inches='tight',dpi=300)

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