#!/usr/bin/env python3
import sys,image,numpy as np

imdata = image.image(sys.argv[-1]).imdata.flatten()
print(np.count_nonzero(imdata==0),"out of",len(imdata),"voxels are zero.")
