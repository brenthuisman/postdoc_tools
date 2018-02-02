import os,subprocess

local_pinnacle_dir = r"Z:\brent\pinnacle_dump"
dosia_exe = r"D:\postdoc\code\Dosia\trunk\src\Win64\Release\Dosia.exe"
outdir = r"Z:\brent\dosia_dump"

with open(os.path.join(local_pinnacle_dir,'purls.txt'),'r') as purls:
    for line in purls.readlines():
        if 'Epid' in line:
            continue
        cmd=dosia_exe+' /beam '+line+' /outdir '+outdir
        print( cmd )
        #os.popen( cmd )
        subprocess.check_call( cmd )

