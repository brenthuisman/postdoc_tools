#!/usr/bin/env python3
import sys,os

infile1 = sys.argv[-3]
infile2 = sys.argv[-2]
outfile = sys.argv[-1]

os.popen("clitkSetBackground -i "+infile1+" -m "+infile2+" -o "+outfile)

