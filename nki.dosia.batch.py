import os,subprocess

#for i in sorted(set([x[0] for x in os.walk('.')])):

stuff="D:\\postdoc\\analyses\\dosia\\dumps_20180110"
stuff="D:\\postdoc\\analyses\\dosia\\dumps_20180111_manual"

for root,dirs,files in os.walk(stuff):
    if root.count(os.sep) == stuff.count(os.sep) + 2:
        cmd="dosia.exe -i "+root
        print( cmd )
        #os.popen( cmd )
        subprocess.check_call( cmd )

