import seaborn as sns,plot,pandas as pd

def gamma2dataframe(results,columntitles=None):
	#is generic for lists of strings where key=val pairs are space separated
	# example results output: Studieset=CaseX Files=1.xdr;2.xdr Mean=0.01 ppc<1=100.00 p99=0.15 p95=0.07 Max=0.43 Min=0.00
	if columntitles==None:
		columntitles = [item.split('=')[0] for item in results[0].split()]
	data = []
	for line in results:
		row=[]
		for item in line.split():
			try:
				row.append(float(item.split('=')[-1]))
			except ValueError:
				row.append(item.split('=')[-1])
		data.append(row)
	return pd.DataFrame(data = data,columns = columntitles)

def cols2dataframe(columntitles,*coldata,**kwargs):
	data = []
	for i,_ in enumerate(coldata[0]):
		if 'metadata' in kwargs:
			row = kwargs['metadata'][:]
		else:
			row=[]
		for cold in coldata:
			row.append(float(cold[i]))
		data.append(row)
	return pd.DataFrame(data = data,columns = columntitles)

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

def fieldseries(df,fname):
	assert( isinstance(df, pd.DataFrame) )
	try:
		pass# del df['Files']
	except:
		pass# print("Deleting of 'Files' column failed: either not present or changed name!")

	sns.set_style(style="whitegrid")
	f, ((ax1,ax2),(ax3,ax4)) = plot.subplots(nrows=2, ncols=2, sharex=False, sharey=False)

	# sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='X' and Generator=='gpumcd'"), ax=ax1, lw=1)#, linestyle='dashed')
	# sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='Y' and Generator=='gpumcd'"), ax=ax2, lw=1)
	# #sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='relY'"), ax=ax3, lw=1)
	# sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='Z' and Generator=='gpumcd'"), ax=ax4, lw=1)

	sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='X'"), style="Generator", ax=ax1, lw=1)#, linestyle='dashed')
	sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='Y' and Generator=='gpumcd'"), ax=ax2, lw=1)
	#sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='relY'"), ax=ax3, lw=1)
	sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='Z' and Generator=='gpumcd'"), ax=ax4, lw=1)

	for ax in (ax1,ax2,ax3,ax4):
		for line in ax.get_lines():
			line.set_dashes([2, 2])

	# sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='X' and Generator=='pinnacle'"), ax=ax1, lw=1)#, linestyle='dashed')
	# sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='Y' and Generator=='pinnacle'"), ax=ax2, lw=1)
	# sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='relY' and (Setname=='10cm' or Setname=='15cm')"), ax=ax3, lw=1)
	# sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='Z' and Generator=='pinnacle'"), ax=ax4, lw=1)

	ax1.set_xlim(-70,70)
	# ax2.set_xlim(-70,70)
	ax3.set_xlim(-70,70)
	ax4.set_xlim(-70,70)

	# ax3.set_ylim(-0.05,0.2)
	ax3.set_ylim(-.25,0.5)

	ax1.set_title("X")
	ax2.set_title("Y")
	ax3.set_title("reldiff X") #relY is relative y over X axis
	ax4.set_title("Z")

	ax3.set_ylabel("Relative Dose")

	ax1.legend_.remove()#.legend().set_title('Fieldsize')
	ax2.legend(title="Fieldsize", loc='upper right', bbox_to_anchor=(1.4, 1.),frameon=False)
	#ax3.legend_.remove()#.legend().set_title('Fieldsize')
	ax4.legend_.remove()#.legend().set_title('Fieldsize')

	f.subplots_adjust(hspace=.5,wspace=.5)
	f.savefig(fname+'.pdf', bbox_inches='tight')
	f.savefig(fname+'.png', bbox_inches='tight',dpi=300)


def profiles(imlist,fname):
	#TODO zie analysis.gpumcd.dose5.py
	#im = image.image(imlist[0])
	#im.getprofile('x')
	return
