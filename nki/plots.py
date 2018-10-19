import seaborn as sns,plot,pandas as pd,numpy as np,scipy

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
	f = sns.catplot(y="value", x="Studyset", col="variable", data=df, kind="box", sharey=False,col_wrap=3)
	f.set_axis_labels("", "Difference")
	if studyset_split==False:
		del df['Studyset']
		# f, ax = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
		# ax = sns.boxplot(y="value", x="variable", data=df)
		f = sns.catplot(y="value", x=None, col="variable", data=df, kind="box", sharey=False,col_wrap=3)
		f.set_axis_labels("", "Difference")
		f.savefig(fname+'.pdf', bbox_inches='tight')
		f.savefig(fname+'.png', bbox_inches='tight',dpi=300)
	else:
		f.savefig(fname+'.split.pdf', bbox_inches='tight')
		f.savefig(fname+'.split.png', bbox_inches='tight',dpi=300)

def fieldseries(df,fname):
	assert( isinstance(df, pd.DataFrame) )

	sns.set_style(style="whitegrid")
	f, ((ax1,ax2),(ax3,ax4)) = plot.subplots(nrows=2, ncols=2, sharex=False, sharey=False)

	df=df.query("Setname=='5cm' or Setname=='10cm' or Setname=='15cm' or Setname=='20cm'")

	sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='X'"), style="Generator", ax=ax1, lw=1)
	sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='Y'"), style="Generator", ax=ax2, lw=1)
	sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='ratY'"), ax=ax3, lw=1)
	# sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='relY'"), style="Generator", ax=ax3, lw=1)
	sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='Z'"), style="Generator", ax=ax4, lw=1)

	ax1.set_xlim(-170,170)
	# ax2.set_xlim(-170,170)
	ax3.set_xlim(-170,170)
	ax4.set_xlim(-170,170)

	# ax3.set_ylim(-.25,0.5)
	ax3.set_ylim(0,2)

	ax1.set_title("X (BLD:Jaw)")
	ax2.set_title("Y")
	# ax3.set_title("reldiff X") #relY is relative y over X axis
	ax3.set_title("ratio X") #relY is relative y over X axis
	ax4.set_title("Z (BLD:MLC)")

	ax3.set_ylabel("Relative Dose")
	ax3.set_ylabel("Dose Ratio")

	ax1.legend(title="Fieldsize", loc='upper right', bbox_to_anchor=(1.4, 1.),frameon=False)
	ax2.legend_.remove()#.legend().set_title('Fieldsize')
	ax3.legend(title="Fieldsize", loc='upper right', bbox_to_anchor=(1.4, 1.),frameon=False)
	ax4.legend_.remove()#.legend().set_title('Fieldsize')

	f.subplots_adjust(hspace=.6,wspace=.5)
	f.savefig(fname+'.pdf', bbox_inches='tight')
	f.savefig(fname+'.png', bbox_inches='tight',dpi=300)

def fieldseries_blok(df,fname):
	assert( isinstance(df, pd.DataFrame) )

	sns.set_style(style="whitegrid")
	f, ((ax1,ax2),(ax3,ax4)) = plot.subplots(nrows=2, ncols=2, sharex=False, sharey=False)

	sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='X'"), ax=ax1, lw=1)
	sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='Y'"), ax=ax2, lw=1)
	sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='ratY'"), ax=ax3, lw=1)
	# sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='relY'"), ax=ax3, lw=1)
	sns.lineplot(x="Distance to isoc [mm]", y="Dose [cGy]", hue="Setname", data=df.query("Axis=='Z'"), ax=ax4, lw=1)

	ax1.set_xlim(-70,70)
	# ax2.set_xlim(-70,70)
	ax3.set_xlim(-70,70)
	ax4.set_xlim(-70,70)

	# ax3.set_ylim(-.25,0.5)
	ax3.set_ylim(0,2)

	ax1.set_title("X (BLD:Jaw)")
	ax2.set_title("Y")
	# ax3.set_title("reldiff X") #relY is relative y over X axis
	ax3.set_title("ratio X") #relY is relative y over X axis
	ax4.set_title("Z (BLD:MLC)")

	# ax3.set_ylabel("Relative Dose")
	# ax3.set_ylabel("Dose Ratio")

	ax1.legend(title="Fieldsize", loc='upper right', bbox_to_anchor=(1.4, 1.),frameon=False)
	ax2.legend_.remove()#.legend().set_title('Fieldsize')
	ax3.legend(title="Relative to Pinnacle", loc='upper right', bbox_to_anchor=(1.4, 1.),frameon=False)
	ax4.legend_.remove()#.legend().set_title('Fieldsize')

	f.subplots_adjust(hspace=.6,wspace=.5)
	f.savefig(fname+'.pdf', bbox_inches='tight')
	f.savefig(fname+'.png', bbox_inches='tight',dpi=300)

def get_penumbras(df):

    def get_profiles_as_ndarray(df,colname,x,y):
        vals = df[colname].unique()
        # print(vals)
        for i,val in enumerate(vals):
            # print( df.groupby(colname).get_group(val) )
            retval = df.groupby(colname).get_group(val)

            for col in retval:
                # print (col)
                if not col in [x,y]:
                    # print ("ifnotin",col)
                    del retval[col]

            yield val,retval[x].values,retval[y].values #y col as numpy array

    for dataset,x,y in get_profiles_as_ndarray(df,"Setname","Distance to isoc [mm]","Dose [cGy]"):
        # print( x[0],x[-1])
        x_intpol = np.linspace(x[0],x[-1],2e4,endpoint=True) #domain where to interpolate
        y_intpol_func = scipy.interpolate.interp1d(x,y) #return interpolated function, linear
        y_intpol = y_intpol_func(x_intpol) #interpolate for x_intpol

        p20 = y.max()*0.2
        p80 = y.max()*0.8

        penum_rechts20 = len(x_intpol)-1
        penum_rechts80 = len(x_intpol)-1
        penum_links20 = 0
        penum_links80 = 0
        while y_intpol[penum_rechts20] < p20:
            penum_rechts20-=1
        while y_intpol[penum_rechts80] < p80:
            penum_rechts80-=1
        while y_intpol[penum_links20] < p20:
            penum_links20+=1
        while y_intpol[penum_links80] < p80:
            penum_links80+=1

        penum_links = abs( x_intpol[penum_links80] - x_intpol[penum_links20] )
        penum_rechts = abs( x_intpol[penum_rechts80] - x_intpol[penum_rechts20] )

        yield(dataset,penum_links,penum_rechts)
