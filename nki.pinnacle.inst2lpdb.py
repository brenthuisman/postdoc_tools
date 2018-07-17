import sys,os
from nki import pinnacle

instfile = sys.argv[-1]
assert instfile.lower().endswith("institution")
lpdbfile = instfile.lower()[:-len("institution")]+"LPDB"
print("Converting",instfile,"to",lpdbfile,".")
if os.path.isfile(lpdbfile):
	lpdbbak = lpdbfile+'.bak'
	print("Renaming existing",lpdbfile,"to",lpdbbak)
	os.rename(lpdbfile,lpdbbak)

pinnacle.make_lpdb([instfile],lpdbfile)
