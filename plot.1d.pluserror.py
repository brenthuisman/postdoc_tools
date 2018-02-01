#!/usr/bin/env python3
import numpy,sys,matplotlib.pyplot as plt,math,operator

## THIS PLOTS Standard Dev, NOT Variance

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
		err_min = []
		err_plus = []
		#nr = 113*57600000
		nr = 600*28800000
		for line in header:
			newline = line.strip()
			newline = float(newline.split()[-1])# * nr
			data.append( newline )
			#data.append( newline )
			#err.append( math.sqrt( nr*float( newline.split()[-1] ) ) / nr 
			err=0
			try:
				err = math.sqrt( newline ) * 1./math.sqrt(nr)
				#err = math.sqrt( newline )
			except:
				pass
			err_min.append( newline - err )
			err_plus.append( newline + err )
			#print err_min
		#print err
		plt.plot(data, label=filename)
		#plt.plot(err_min, label=filename)
		#plt.plot(err_plus, label=filename)
		#print data, err_min, err_plus, '\n'
		plt.fill_between(list(range(len(data))), err_min, err_plus, alpha=0.25)
	if filename.endswith('.raw'):
		data = numpy.fromfile(filename, dtype='<f4')
		plt.plot(data, label=filename)
	#plt.plot(data, label=filename)
	plt.ylabel('Counts')
	plt.ylabel('PG energy')
	#plt.legend(loc=4,prop={'size':6})
	plt.legend(prop={'size':10})
	plt.savefig(fileout)