#!/usr/bin/env python3
import sys,os

infile = sys.argv[-1]
outfile = infile+".modified.mhd"

#get cuts, or set default.
#default is reading the .mhd header and actually not cutting at all.
#cuts = sys.argv[-2]

#get dimensions and set full image as default
cuts = os.popen("clitkImageInfo "+infile).readlines()[0].split()[2].split('x')

#apply cuts
cuts = ','.join(['0,'+str(int(x)-1) for x in cuts])
os.popen("clitkCropImage -i "+infile+" -o "+outfile+" --boundingBox="+cuts)



#call(["clitkCropImage","-i",self.imagefile,"-o",self.imagefile,"--boundingBox=x1,x2,y1,y2,z1,z2"])

#call(["clitkImageConvert","-i",self.imagefile,"-o",self.imagefile,"-c"])

