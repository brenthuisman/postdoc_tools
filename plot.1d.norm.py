#!/usr/bin/env python3
import numpy,sys,matplotlib.pyplot as plt,dump

#print plt.style.available
#plt.style.use('ggplot')

if len(sys.argv) < 3:
	print("Specify at least one input and one output.")
	sys.exit()
filesin = sys.argv[1:-1]
fileout = sys.argv[-1]
for filename in filesin:
	if filename.endswith('.txt'):
		header = open(filename,'r')
		data = []
		for line in header:
			newline = line.strip()
			data.append(float(newline.split()[-1]))
			
	if filename.endswith('.raw'):
		data = numpy.fromfile(filename, dtype='<f4')

	maxi=max(data)
	plt.plot([x/maxi for x in data], label=filename)
	#plt.plot(data, label=filename)
	plt.ylabel('Counts')
	plt.ylabel('PG energy')
	#plt.legend(loc=4,prop={'size':6})
	plt.legend(prop={'size':10},loc='best')
	plt.savefig(fileout)
