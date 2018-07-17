import collections,image,seaborn as sns,pandas as pd

#TODO REPLACE
def boxplot_gamma2(results,fname,showoutliers=False,flat=False):
	if not isinstance(results, list):
		print("Boxplots for a single point is a bit strange, but since I am both omnipotent and good humoured, I shall do as you please.")
		results = [results]

	data = collections.defaultdict(list)
	for line in results:
		for item in line.split():
			data[item.split('=')[0]].append(float(item.split('=')[-1]))

	if flat:
		f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
		ax1.boxplot( data.values() , labels=data.keys() , showfliers=showoutliers,  showmeans=True, meanline = True )
		ax1.set_yscale('log')
	else:
		f, axes = plot.subplots(nrows=2, ncols=3, sharex=False, sharey=False)
		for index,(dat,val) in enumerate(zip(data.values(),data.keys())):
			axes[ index//3 , index%3 ].boxplot( dat , showfliers=showoutliers)#, showmeans=True)#, meanline = True )
			axes[ index//3 , index%3 ].set_title(val)
			#axes[ index//3 , index%3 ].set_yscale('log')

	f.savefig(fname+'.pdf', bbox_inches='tight')
	f.savefig(fname+'.png', bbox_inches='tight',dpi=300)
	plot.close('all')

	with open(fname+'.txt','w') as resultfile:
		# resultfile.writelines([i+': '+j for i,j in zip(cases,results_pinpin)])
		resultfile.writelines([l+'\n' for l in results])

def boxplot_gamma(df,fname):
	assert( isinstance(df, pd.DataFrame) )
	try:
		del df['Files']
	except:
		print("Deleting of 'Files' column failed: either not present or changed name!")
	df = pd.melt(df,id_vars=["Studieset"])# de rest: ,value_vars=[''])
	print(df)
	# f = sns.factorplot(y="value", hue="Studieset", col="variable", data=df, palette="PRGn")
	f = sns.factorplot(y="value", x="Studieset", col="variable", data=df, kind="box", sharey=False,col_wrap=3)
	f.set_axis_labels("", "Percentage Difference")
	f.savefig(fname+'.pdf', bbox_inches='tight')
	f.savefig(fname+'.png', bbox_inches='tight',dpi=300)
	# sns.factorplot(x="variable", y="value", hue="Studieset", col="variable", data=df, palette="PRGn")

def profiles(imlist,fname):
	#TODO zie analysis.gpumcd.dose5.py
	#im = image.image(imlist[0])
	#im.getprofile('x')
	return
