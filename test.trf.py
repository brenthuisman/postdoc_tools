import trf

fn=r"D:\postdoc\analyses\linaclog\testfiles_jochem\15-08-17 05_25_02 Z 1_Bundel 1.trf"

header,table=trf.read_trf(fn)
print(header)
print("================")
print(table)