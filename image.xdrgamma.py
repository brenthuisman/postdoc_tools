#import image
from nki.runners import calcgamma

for i in range(1,6):
	i1 = f"D:/postdoc/analyses/testbrent3/{i}.gpumcd.xdr"
	i2 = f"D:/postdoc/analyses/testbrent3/{i}.gpumcd.xdr"
	outf = f"D:/postdoc/analyses/testbrent3/{i}.gammamap.xdr"
	calcgamma(i1,i2,outf)