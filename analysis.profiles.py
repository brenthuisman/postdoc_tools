#!/usr/bin/env python3
import numpy as np,sys,image,seaborn as sns,plot,argparse,glob,pandas as pd
from os import path
from nki import plots
# from nki import runners

# imagefiles = [r"Z:\brent\stijn\pindump_nooverrides\MonacoPhantom\A.trialname.1.beam\dose.mhd",r"Z:\brent\stijn\pindump_nooverrides\MonacoPhantom\A.trialname.1.beam\gpumcd_dose.mhd"]

parser = argparse.ArgumentParser(description='specify mulitple mhd images to analyse')
parser.add_argument('--dir',default="")
parser.add_argument('--noupdate',action='store_true')
opt = parser.parse_args()

fname = path.join(opt.dir,'profile_plot')
setnames = ["2cm","3cm","4cm","5cm","6cm","8cm","10cm","15cm","20cm","23cm"]

if not opt.noupdate:
    ## lets make csv
    imagefiles = glob.glob(path.join(opt.dir,"**","*dose.mhd"), recursive=True)
    assert(len(setnames)*2==len(imagefiles))
    images = [image.image(i) for i in imagefiles]

    listoframes=[]
    for i,setname in enumerate(setnames):
        pin_im = image.image( imagefiles[int(2*i)] )
        gpumcd_im = image.image( imagefiles[int(2*i+1)] )

        x_x = pin_im.get_axis_mms('x') #same for all
        x_y = pin_im.get_axis_mms('y') #same for all
        x_z = pin_im.get_axis_mms('z') #same for all

        pdd_max = pin_im.getline('y').argmax()

        py_x = pin_im.getline_atindex('x',pdd_max)
        py_y = pin_im.getline('y')
        py_z = pin_im.getline_atindex('z',pdd_max)
        gy_x = gpumcd_im.getline_atindex('x',pdd_max)
        gy_y = gpumcd_im.getline('y')
        gy_z = gpumcd_im.getline_atindex('z',pdd_max)

        y_xrel = ( gy_x - py_x ) / py_x

        columntitles = ["Setname","Generator","Axis",'Distance to isoc [mm]','Dose [cGy]']
        listoframes.append( plots.cols2dataframe(columntitles,x_x,py_x,metadata=[setname,'pinnacle','X']) )
        listoframes.append( plots.cols2dataframe(columntitles,x_y,py_y,metadata=[setname,'pinnacle','Y']) )
        listoframes.append( plots.cols2dataframe(columntitles,x_z,py_z,metadata=[setname,'pinnacle','Z']) )
        listoframes.append( plots.cols2dataframe(columntitles,x_x,gy_x,metadata=[setname,'gpumcd','X']) )
        listoframes.append( plots.cols2dataframe(columntitles,x_y,gy_y,metadata=[setname,'gpumcd','Y']) )
        listoframes.append( plots.cols2dataframe(columntitles,x_z,gy_z,metadata=[setname,'gpumcd','Z']) )
        listoframes.append( plots.cols2dataframe(columntitles,x_x,y_xrel,metadata=[setname,'reldiff','relY']) )

        # columntitles = ["x_x","x_y","x_z","py_x","py_y","py_z","gy_x","gy_y","gy_z","y_xrel"]
        # listoframes.append( plots.cols2dataframe(columntitles,setnames,x_x,x_y,x_z,py_x,py_y,py_z,gy_x,gy_y,gy_z,y_xrel) )

    df = pd.concat(listoframes)
    df.to_csv(fname+".csv")
    # print(df)

## lets plot csv
df = pd.read_csv(fname+".csv",index_col=0)

plots.fieldseries(df,fname)

# Finish: stijns profielen
# runners.execute(r"D:\postdoc\code\xdr_xdr2mhd\src\Win32\Debug\xdr_xdr2mhd.exe","/in blabla.xdr")
