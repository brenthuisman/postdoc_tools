#!/usr/bin/env python3
import sys,image
from subprocess import call

if len(sys.argv) < 2:
	print("Specify a maskfile.")
	sys.exit()

maskfile = sys.argv[-1]

#might as well convert to float so all our images are the same.
call(["clitkImageConvert","-i",maskfile,"-o","finalmask.mhd","-t","float"])
#call(["clitkImageArithm","-s","1","-t","1","-i",maskfile,"-o",maskfile])

print(maskfile, "converted.")