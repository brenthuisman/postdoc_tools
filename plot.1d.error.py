#!/usr/bin/env python3
import numpy,sys,matplotlib.pyplot as plt,math,operator

## THIS PLOTS Standard Dev, NOT Variance

#print plt.style.available
#plt.style.use('ggplot')

#nrprim = float(600*28800000)
nrprim = float(1e6)

if len(sys.argv) < 3:
	print("Specify at least one input and one output.")
	sys.exit()
filesin = sys.argv[1:-1]
fileout = sys.argv[-1]
for filename in filesin:
	if filename.endswith('.txt'):
		header = open(filename,'r')
		errdata = []
		for line in header:
			newline = line.strip()
			newline = float(newline.split()[-1])# * nr
			err=0
			if newline > 0.:
				err = math.sqrt( newline/nrprim ) # == math.sqrt( newline ) / newline
			else:
				err = math.sqrt( 1./nrprim )
			errdata.append( err )
		plt.plot(errdata[:], label=filename)
	if filename.endswith('.raw'):
		rawfilenames = filename.split(":")
		data = numpy.fromfile(rawfilenames[0], dtype='<f4').tolist()
		if len(rawfilenames) > 1:
			plt.plot([math.sqrt(i/nrprim) for i in data], label=filename)
		else:
			plt.plot([math.sqrt(i) for i in data], label=filename)
	#plt.plot(data, label=filename)
	plt.ylabel('Counts')
	plt.ylabel('PG energy')
	#plt.legend(loc=4,prop={'size':6})
	plt.legend(prop={'size':10})
	plt.savefig(fileout)