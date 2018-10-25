#!/usr/bin/env python3
import numpy as np,sys,image,seaborn as sns,plot,argparse,glob,pandas as pd
from os import path
from nki import plots
# from nki import runners

parser = argparse.ArgumentParser(description='specify mulitple mhd images to analyse')
parser.add_argument('--dir',default=r"Z:\brent\fieldseries\F180813B")
parser.add_argument('--noupdate',action='store_true')
opt = parser.parse_args()

# isoc in plan.dump. here multiplied x,y coords with -1.
if 'F180813B' in opt.dir:
    isoc = [-0.165627,-16.8293,-0.299999]
if 'F180823Q' in opt.dir:
    isoc = [-3.71,-16.8293,-0.299999]

print("isoc",isoc)

fname = path.join(opt.dir,'profile_plot')
setnames = ["2cm","23cm","3cm","4cm","5cm","6cm","8cm","10cm","15cm","20cm"] #23 is sorted here.

if not opt.noupdate:
    ## lets make csv
    imagefiles = sorted(glob.glob(path.join(opt.dir,"**","*dose.mhd"), recursive=True))
    try:
        assert(len(setnames)*2==len(imagefiles))
    except AssertionError as e:
        print(e)
        print(setnames)
        print(imagefiles)

    print([s+' '+i for s,i in zip(setnames,imagefiles[::2])])

    listoframes=[]
    for i,setname in enumerate(setnames):
        pin_im = image.image( imagefiles[int(2*i)] )
        gpumcd_im = image.image( imagefiles[int(2*i+1)] )
        print ('loading',imagefiles[int(2*i)],setname)
        # print('pixelsize',pin_im.header['DimSize'])
        # shift_half_pixel = False
        # print ('x',pin_im.get_axis_mms('x',shift_half_pixel)[0]," ",pin_im.get_axis_mms('x',shift_half_pixel)[-1])
        # print ('y',pin_im.get_axis_mms('y',shift_half_pixel)[0]," ",pin_im.get_axis_mms('y',shift_half_pixel)[-1])
        # print ('z',pin_im.get_axis_mms('z',shift_half_pixel)[0]," ",pin_im.get_axis_mms('z',shift_half_pixel)[-1])

        # print(pin_im.header['Offset'][1],pin_im.header['ElementSpacing'][1],pin_im.header['DimSize'][1])


        # print(-344+270-2)
        # print(len(pin_im.get_axis_mms('y'))*2)
        # quit()

        isoc_index = pin_im.coord2index([i*10 for i in isoc],True) #mm to cm
        print ("isoc_index",isoc_index)
        isoc_index = [88, 83, 68]
        isoc = [2./10., -169./10., 3./10.]
        # echte index is [88, 83, 68], uitgaande van 10cm diep (wat voor EPID calib veldserie metingen altijd zo is)

        x_x = [x-isoc[0]*10 for x in pin_im.get_axis_mms('x')]
        x_y = [x-isoc[1]*10 for x in pin_im.get_axis_mms('y')]
        x_z = [x-isoc[2]*10 for x in pin_im.get_axis_mms('z')]

        py_x = pin_im.getline_atindex('x',isoc_index[1],isoc_index[0])
        py_y = pin_im.getline_atindex('y',isoc_index[2],isoc_index[0])
        py_z = pin_im.getline_atindex('z',isoc_index[2],isoc_index[1])
        gy_x = gpumcd_im.getline_atindex('x',isoc_index[1],isoc_index[0])
        gy_y = gpumcd_im.getline_atindex('y',isoc_index[2],isoc_index[0])
        gy_z = gpumcd_im.getline_atindex('z',isoc_index[2],isoc_index[1])

        y_xrel = ( gy_x - py_x ) / py_x
        y_xrat = gy_x / py_x

        print("len",len(x_x),len(py_x))

        columntitles = ["Setname","Generator","Axis",'Distance to isoc [mm]','Dose [cGy]']
        listoframes.append( plots.cols2dataframe(columntitles,x_x,py_x,metadata=[setname,'pinnacle','X']) )
        listoframes.append( plots.cols2dataframe(columntitles,x_y,py_y,metadata=[setname,'pinnacle','Y']) )
        listoframes.append( plots.cols2dataframe(columntitles,x_z,py_z,metadata=[setname,'pinnacle','Z']) )
        listoframes.append( plots.cols2dataframe(columntitles,x_x,gy_x,metadata=[setname,'gpumcd','X']) )
        listoframes.append( plots.cols2dataframe(columntitles,x_y,gy_y,metadata=[setname,'gpumcd','Y']) )
        listoframes.append( plots.cols2dataframe(columntitles,x_z,gy_z,metadata=[setname,'gpumcd','Z']) )
        listoframes.append( plots.cols2dataframe(columntitles,x_x,y_xrel,metadata=[setname,'reldiff','relY']) )
        listoframes.append( plots.cols2dataframe(columntitles,x_x,y_xrat,metadata=[setname,'ratio','ratY']) )

    df = pd.concat(listoframes)
    df.to_csv(fname+".csv")
    # print(df)

## lets plot csv
df = pd.read_csv(fname+".csv",index_col=0)

plots.fieldseries(df,fname)
