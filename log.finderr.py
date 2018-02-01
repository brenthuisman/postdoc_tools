#!/usr/bin/env python3

'''
Checks for gatejobs files that miss an output dir.
'''

import sys,os,re
from collections import Counter as cntr

gatelogs = glob.glob("./**/gatejob.*")
outdirs = glob.glob("./**/output.*")
w = '((?<!libg4)error|terminated|warning|PBS:|exceeded limit)' #dont match libG4error

print(len(gatelogs), "gatelogs found.", len(outdirs), "output dirs found.")

if len(gatelogs) == len(outdirs):
	print("All appears in order. Exiting...")
	sys.exit(0)

gatelog_ids = set([int(x.split('/')[-1].split('.o')[-1]) for x in gatelogs])
outdir_ids = set([int(x.split('/')[-1].split('.')[-1]) for x in outdirs])

errlist = list(gatelog_ids - outdir_ids)

gatelogs_werr = []
for x in errlist:
	#print x
	gatelogs_werr.extend(glob.glob("./**/gatejob*"+str(x)))

print("--------------Joblogs with errors----------------")
print("joblogs without matching outputdir:")
for logf in gatelogs_werr:
	print(logf)
	with open(logf) as f:
		preverr=""
		for line in f:
			if re.search(w,line,re.IGNORECASE) and preverr!=line:
				preverr=line
				print(line, end=' ')

print("-------------------------------------------------")

run_ids=[]
if len(gatelogs_werr[0].split('/')) > 2:
	for logf in gatelogs_werr:
		run_ids.append( logf.split('/')[-2] )

	for key,val in list(cntr(run_ids).items()):
		print("Relaunch", val, "jobs in", key)
else:
	print("Relaunch", len(gatelogs)-len(outdirs),"jobs.")
