#!/usr/bin/env python3
import sys,datetime,tableio
from collections import Counter

def parselog(filename):
	logfile = open(filename,'r')
	mycounter = Counter()
	for line in logfile.readlines():
		if line.startswith("Brent "):
			#print line
			#print line.split()[-1]
			mycounter[line.split()[-1]] += 1
	logfile.close()
	return mycounter

print((parselog(sys.argv[-1])))
