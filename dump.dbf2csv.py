import sys
import csv
from dbfread import DBF

fname = sys.argv[-1]
assert fname.lower().endswith('.dbf')
outname = fname.lower()[:-4]+".csv"
print("Converting",fname,"to",outname,".")

table = DBF(fname)

with open(outname,'w',newline='') as f:
	writer = csv.writer(f)
	writer.writerow(table.field_names)
	for record in table:
		writer.writerow(list(record.values()))
