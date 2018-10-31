#!/usr/bin/env python3
import numpy as np,sys,image,seaborn as sns,plot,argparse,glob,pandas as pd
from os import path
from nki import plots

parser = argparse.ArgumentParser(description='specify mulitple mhd images to analyse')
parser.add_argument('--noupdate',action='store_true')
opt = parser.parse_args()

# isoc in plan.dump. multiply y,z coords with -1.
isoc = [0.31,-4.68,-0]

fname = path.join(r"Z:\brent\stijn\__results\blok\minus_stijnpin",'profile_plot')

if not opt.noupdate:
    ## lets make csv
    imagefiles = [r"Z:\brent\stijn\pindump_nooverrides\MonacoPhantom\sum_dose.factor.mhd",
    r"Z:\brent\stijn\pindump_nooverrides\MonacoPhantom\sum_gpumcd_dose.factor.mhd",
    r"Z:\brent\stijn\dicom\blokmon.xdr.setongrid.xdr.mhd"]

    setnames = ["Pinnacle","Dosia","Monaco"]

    listoframes=[]
    for i,setname in enumerate(setnames):
        im = image.image( imagefiles[i] )

        x_x,x_y,x_z = im.get_axes_labels()
        isoc_index = im.get_pixel_index([i*10 for i in isoc],False) #mm to cm, no halfpixel
        y_x,y_y,y_z = im.get_profiles_at_index(isoc_index)
        x_x = [x-isoc[0]*10 for x in x_x]
        x_y = [x-isoc[1]*10 for x in x_y]
        x_z = [x-isoc[2]*10 for x in x_z]

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
