import collections,image,seaborn as sns,matplotlib.pyplot as plt,pandas as pd

def gamma2dataframe(results,columns=None):
	#is generic for lists of strings where key=val pairs are space separated
	# example results output: Studieset=CaseX Files=1.xdr;2.xdr Mean=0.01 ppc<1=100.00 p99=0.15 p95=0.07 Max=0.43 Min=0.00
	if columns==None:
		columns = [item.split('=')[0] for item in results[0].split()]
	data = []
	for line in results:
		row=[]
		for item in line.split():
			try:
				row.append(float(item.split('=')[-1]))
			except ValueError:
				row.append(item.split('=')[-1])
		data.append(row)
	return pd.DataFrame(data = data,columns = columns)

def boxplot_gamma(df,fname,studyset_split=True):
	assert( isinstance(df, pd.DataFrame) )
	try:
		del df['Files']
	except:
		print("Deleting of 'Files' column failed: either not present or changed name!")
	df = pd.melt(df,id_vars=["Studyset"])# de rest: ,value_vars=[''])
	if studyset_split==False:
		del df['Studyset']

	print(df)

	f = sns.catplot(y="value", x="Studyset", col="variable", data=df, kind="box", sharey=False,col_wrap=3)
	f.set_axis_labels("", "Difference")
	# f, ax = plt.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
	# ax = sns.boxplot(y="value", x="variable", data=df)

	f.savefig(fname+'.pdf', bbox_inches='tight')
	f.savefig(fname+'.png', bbox_inches='tight',dpi=300)

def profiles(imlist,fname):
	#TODO zie analysis.gpumcd.dose5.py
	#im = image.image(imlist[0])
	#im.getprofile('x')
	return
