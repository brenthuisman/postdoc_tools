#!/usr/bin/env python3
import image,argparse
from os import path

parser = argparse.ArgumentParser(description='specify mulitple mhd images to analyse')
parser.add_argument('inputimage')
opt = parser.parse_args()

print('Converting',path.abspath(opt.inputimage))

im = image.image(path.abspath(opt.inputimage))
if opt.inputimage.endswith('.mhd'):
    im.saveas(path.abspath(opt.inputimage)+'.xdr')
elif opt.inputimage.endswith('.xdr'):
    im.saveas(path.abspath(opt.inputimage)+'.mhd')
else:
    print('No valid input image specified. Aborting...')