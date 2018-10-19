#!/usr/bin/env python3
import numpy as np,sys,image,seaborn as sns,plot,argparse,glob,pandas as pd
from os import path
from nki import plots

parser = argparse.ArgumentParser(description='specify mulitple mhd images to analyse')
parser.add_argument('--noupdate',action='store_true')
opt = parser.parse_args()

# isoc in plan.dump. multiply x,y coords with -1.
isoc = [-0.31,-4.68,0]

fname = path.join(r"Z:\brent\stijn\__results\blok\minus_stijnpin",'profile_plot')

if not opt.noupdate:
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

        #NOT swap x,z
        x_x = [x-isoc[0] for x in im.get_axis_mms('x')]
        x_y = [x-isoc[1] for x in im.get_axis_mms('y')]
        x_z = [x-isoc[2] for x in im.get_axis_mms('z')]

        isoc_index = [
            min(range(len(x_x)), key=lambda i: abs(x_x[i]-0)),
            min(range(len(x_y)), key=lambda i: abs(x_y[i]-0)),
            min(range(len(x_z)), key=lambda i: abs(x_z[i]-0)),
        ]

        y_x = im.getline_atindex('x',isoc_index[1],isoc_index[2]) #NOT swap x,z
        y_y = im.getline_atindex('y',isoc_index[0],isoc_index[2])
        y_z = im.getline_atindex('z',isoc_index[0],isoc_index[1])

        # pdd_max = im.getline('y').argmax()
        # if glob_y_x is None:
        #     pdd_max = im.get1dlist([1,0,1]).argmax()
        #     center_x = im.get1dlist([1,1,0]).argmax() #x,z indices swapped!!!
        #     center_z = im.get1dlist([0,1,1]).argmax()
        #     print("midden van PDD max:",imagefiles[i],center_x,pdd_max,center_z)
        # y_x = im.getline_atindex('x',pdd_max,center_z)
        # y_y = im.getline_atindex('y',center_x,center_z)
        # y_z = im.getline_atindex('z',center_x,pdd_max)

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
    df.to_csv(fname+".csv")
    # print(df)

## lets plot csv
df = pd.read_csv(fname+".csv",index_col=0)

plots.fieldseries_blok(df,fname)
