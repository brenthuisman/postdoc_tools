import image

orig=image.image("/home/brent/phd/art2_lyso_box/stage2_box15/data/source-160.mhd")

###########
try:
	im0=orig.copy()
except:
	im0=image.image("/home/brent/phd/art2_lyso_box/stage2_box15/data/source-160.mhd")
im0.imdata[0:50,:,:,:] = 0
#im0.saveas("/home/brent/phd/art2_lyso_box/tmp/source-160-0.mhd")

#this image has FOP at x=+50mm. We want to zero out in a window of +/-5cm around this point. Since we dont have to zero out post FOP (is already zero), we just need to zero all negative X voxels. NOTE, image is 4D.
###########
energy_cuttoff = 1 #in MEV
orig.imdata[:,:,:,:int(250/10*energy_cuttoff)] = 0
im0.imdata[:,:,:,:int(250/10*energy_cuttoff)] = 0

try:
	print(orig.getsum())
	print(im0.getsum())
except:
	print(orig.sum())
	print(im0.sum())

im0.saveas("/home/brent/phd/art2_lyso_box/tmp/im0.mhd")

orig.saveas("/home/brent/phd/art2_lyso_box/tmp/orig.mhd")
