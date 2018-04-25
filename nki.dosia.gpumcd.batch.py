import os,subprocess

#dosia_dump = r"Z:\brent\dosia_dump"
dosia_dump = r"Z:\brent\jochempepijn"
#dosia_dump = r"Z:\brent\stijn\pinnacle_dump"
dosia_exe_dir = r"D:\postdoc\code\gpumcd_rtplan\x64\Release"

failed_runs=[]
#errorcodes=[]

for root,dirs,files in os.walk(dosia_dump):
    if root.count(os.sep) == dosia_dump.count(os.sep) + 2:
        cmd=os.path.join(dosia_exe_dir,'dosia.exe')+" -i "+root
        print( cmd )
        try:
            subprocess.check_call( cmd , cwd=dosia_exe_dir)
        except subprocess.CalledProcessError as e:
            failed_runs.append(root+' '+str(e.returncode)+'\n')
            #errorcodes.append(e.returncode)

with open(os.path.join(dosia_dump,'run_fails.txt'),'w') as failfile:
    failfile.writelines(failed_runs)
