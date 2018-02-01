#!/usr/bin/env python3
import numpy,sys,matplotlib.pyplot as plt,operator,pickle

#print plt.style.available
#plt.style.use('ggplot')
nrprim = 600*28800000

if len(sys.argv) < 3:
	print("Specify at least one input and one output. First input is the one the output is relative to.")
	sys.exit()
filesin = sys.argv[1:-1]
fileout = sys.argv[-1]

data = [] #rows=files,column[0]=filename
for filename in filesin:
	datatmp = [filename]
	if filename.endswith('.txt'):
		header = open(filename,'r')
		for line in header:
			newline = line.strip()
			datatmp.append(float(newline.split()[-1]))
	if filename.endswith('.raw'):
		datatmp.extend(numpy.fromfile(filename, dtype='<f4').tolist())
	if filename.endswith('.pylist'):
		datatmp.extend(pickle.load(open(filename)))
	data.append(datatmp)

datanew = []
for dataset in data[::-1]: #start at the end
	datatmp = []
	for index,val in enumerate(dataset):
		if index is 0:
			datatmp.append(val)
			continue #do not modify filename
		try:
			datatmp.append((data[0][index]-val) / data[0][index])
		except ZeroDivisionError:
			datatmp.append(0)
	datanew.append(datatmp)

#for datindex in range(1,len(data)): #start at the end
#	for valindex in range(datindex):
#		if valindex is 0:
#			continue #do not modify filename
#		try:
#			data[datindex][valindex] = (data[0][valindex]-data[datindex][valindex]) / data[0][valindex]
#		except ZeroDivisionError:
#			val = 0

for dataset in datanew:
	plt.plot(dataset[1:], label=dataset[0],alpha=0.5)
	plt.ylabel('Yield')
	#plt.ylabel('PG energy')
	#plt.legend(loc=4,prop={'size':6})
	plt.legend(prop={'size':10})
	plt.savefig(fileout)