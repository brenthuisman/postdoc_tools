#!/usr/bin/env python3
import numpy,sys,matplotlib.pyplot as plt,pickle,dump

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
	if filename.endswith('.pylist'):
		data = pickle.load(open(filename))
	plt.plot(data, label=filename,alpha=0.8)

	#plt.plot(data, label=filename)
	plt.ylabel('Yield')
	#plt.ylabel('PG energy')
	#plt.legend(loc=4,prop={'size':6})
	plt.legend(prop={'size':10},bbox_to_anchor=(1.2, 1.),frameon=False)
	plt.savefig(fileout, bbox_inches='tight')
