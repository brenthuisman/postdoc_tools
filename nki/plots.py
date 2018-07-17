import collections,image,seaborn as sns,pandas as pd

def gamma2dataframe(results):
	# example results output: Studieset=CaseX Files=1.xdr;2.xdr Mean=0.01 ppc<1=100.00 p99=0.15 p95=0.07 Max=0.43 Min=0.00
	columns = ["Studieset","Files","Mean γ","γ passrate","γ99","γ95","Max γ","Min γ"]
	# columns = ["Studieset","Mean G","G passrate","G99","G95","Max dose","Min dose"]
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
