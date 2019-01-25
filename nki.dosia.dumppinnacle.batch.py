import os,subprocess

local_pinnacle_dir = r"Z:\brent\pinnacle_dump"
dosia_exe = r"D:\postdoc\code\Dosia\trunk\src\Win32\Debug\Dosia.exe"
outdir = r"Z:\brent\dosia_dump"

failed_dumps=[]


if not os.path.isdir(outdir):
    os.makedirs(outdir)

with open(os.path.join(local_pinnacle_dir,'purls.txt'),'r') as purls:
    for line in purls.readlines():
        if 'Epid' in line:
            continue
        line = line.replace(':patient_',':Patient_') #yes....
        cmd=dosia_exe+' /beam '+line+' /outdir '+outdir
        print( cmd )
        #os.popen( cmd )
        try:
            subprocess.check_call( cmd )
        except subprocess.CalledProcessError:
            failed_dumps.append(line+'\n')

with open(os.path.join(outdir,'dump_fails.txt'),'w') as failfile:
    failfile.writelines(failed_dumps) #doesnt do newlines
