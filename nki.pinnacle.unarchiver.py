# pip install pyodbc

import pyodbc,configparser,sys,os,time,collections##,re,tarfile

#settings
overwrite = False #overwrite if previous dump in local_pinnacle_dir found
epidclin_basedir = r"W:\Epidclin\EPIDOS\ECR\EVP.INIs\ALL"
local_pinnacle_dir = r"Z:\brent\pinnacle_dump"
local_pinnacle_dbname = "pinnacle_local" #in your datasources.ini
pinnacle_pacs = r"\\172.19.36.17\archive\Kliniek"
zexe = r"D:\postdoc\code\7za.exe"
internal_untar = False #is slower, but no deps.

sqlquery="""SELECT i.ida, t.Field_Name, s.site_name
FROM (
ident i
JOIN txfield t ON i.pat_id1 = t.pat_id1
JOIN site s ON i.pat_id1 = s.Pat_ID1
)
WHERE t.last_tx_dttm > '2017-01-01'
AND t.last_tx_dttm < '2018-01-01' --after last treatment, takes bout a month to be archived and available
AND t.Type_Enum = 13 --VMAT
AND t.MachineCharID IN (262,265,275) --agility
AND t.IsFFF = 0
AND t.Version = 0 -- version=0 is momenteel 'actieve' plan (beam). dit kan dus veranderen! todo: optioneel maken
AND s.Version = 0
AND t.FLD_ID IN (SELECT fld_id FROM txfieldpoint WHERE energy = 6)
AND s.Site_Name LIKE '%<%>%' --w/o upi are nonlinac treatments   
AND i.ida NOT LIKE 'Z%' --Z is not clinical
AND t.Field_Name <> 'NIET' --filthy clinicians dont clean up their messes
AND s.site_name <> 'NIET' --filthy clinicians
AND ISNUMERIC(i.ida) = 1 --normal clinical plans that are irriadiated on patients are numeral only, with letters is for research
ORDER BY i.ida, t.Field_Name, s.site_name ASC;
"""


####################################################################################
# Do not edit below this line
####################################################################################

#LPDB constants

lpdb_header = """SiteName = "AvL/NKI Amsterdam";
InstitutionList ={
  Institution ={"""
lpdb_footer = """  };
};
DefaultInstitution = "Institution_0";
UseBestMountPoint = 0;
DefaultBackupIODevice = "";
NextUniqueInstitutionID = 99;
NextUniquePatientID = 99;
NextUniqueBackupID = 0;
RestoreSolarisData = 1;
CreateNewInstitution = 0;
BackupRestoreDest = "UNIX File";
BackupIndexSortType = "Backup Volume";
TypeOfBackup = "Manual";
BackupCompressed = 0;
BackupDebugOutputEnabled = 0;
AtJobId = "";
AtJobHost = "";
UnattendedBackupSet = 0;
PrintReport = 0;
AddHeaderInfoToIndex = 0;
ReadMultipleHeaders = 0;
TempRestoreDir = "/tmp";
GenerateHTMLIndex = 0;
BackupVolumeNameList ={
};
RestoreSpaceThreshold = 99999.9;
NumBackupInstitutionFiles = 200;
MaxAgeOfBackupInstitutionFiles = 180;

/* 6Ñ */
"""

# Start program

start_time = time.time()

if not os.path.isdir(local_pinnacle_dir):
    os.makedirs(local_pinnacle_dir)

lpdbfile = os.path.join(local_pinnacle_dir,'LPDB')

#run sql query

cnxn = pyodbc.connect(
    r'DRIVER={ODBC Driver 11 for SQL Server};'
    r'SERVER=rtmquery.radim.local\mquery;'
#    r'DATABASE=;'
    r'UID=epid-dos;'
    r'PWD=ep1d-d0s'
    )

cursor = cnxn.cursor()
cursor.execute(sqlquery)
rows = cursor.fetchall()

studydata = collections.defaultdict(dict)
mrn_fails = set()

sys.stderr.write(str(len(rows))+" results in sql query.\n")

#NOOT: currently active patients are NOT YET in the archive. Only when they are deactivated (i.e. their treatment is over), do they appear in the archive.

#find pinnacle urls

for row in rows:
    #print('%s \t %s \t %s' % (row.ida, row.Field_Name, row.site_name))
    
    #nodig voor testsetrunner: ida, upi, in epidos_sql_db: patientid, upi
    upi = str(row.site_name.split('<')[1].split('>')[0])
    mrn = str(row.ida)
    
    filename = os.path.join( epidclin_basedir, mrn+".evp.ini")

    try:
        assert( os.path.isfile(filename) ) #configparser does not throw errors when file not found
        urls=[] #there will be multiple beams(/fields) for a matching TP
        ini1 = configparser.ConfigParser()
        ini1.read(filename)
        #alleen fieldurls (==beamurls) nodig voor dosiadump
        for s in ini1.sections():
            try:
                if mrn in ini1[s]['FieldUrl'] and 'Epid' not in ini1[s]['FieldUrl'] and ini1[s]['Plan'] == upi:
                    urls.append(ini1[s]['FieldUrl'])
            except KeyError:
                pass #skip this section
        if len(urls) == 0:
            raise FileNotFoundError("No Pinnacle Urls for mrn "+mrn+". Skipping...\n")
        #studydata[mrn][upi][urls]=urls
        #studydata[mrn].update({upi:urls})
        studydata[mrn][upi]=urls #other upis with urls may be added later/exist already
    except AssertionError:
        mrn_fails.update({mrn})
        #sys.stderr.write("No entry in epinclin data found for mrn: "+mrn+". Skipping...\n")
    except FileNotFoundError as e:
        mrn_fails.update({mrn})
        #sys.stderr.write(str(e))
    except ValueError as e:
        mrn_fails.update({mrn})
        sys.stderr.write(str(e))

sys.stderr.write(str(len(mrn_fails))+" mrns had no or missing data.\n")
sys.stderr.write(str(len(studydata))+" mrns with full data found.\n")

skipped_arcfiles = []

#first create list of archive mrn folders, then only take latest (it should contain all older info!)

for root, dirs, files in os.walk(pinnacle_pacs):
    #sys.stderr.write(files)
    for filename in files:
        filemrn = filename.split('.')[0]
        #find if theres an archive for this mrn
        if filemrn in studydata:
            new_arcfile = os.path.join(root, filename)
            #try:
                #studydata[filemrn]['arcfile'] #if does not exist, except
            if 'arcfile' in studydata[filemrn]:
                #we already found an archive with this mrn, check for date.
                existing_arcfile = studydata[filemrn]['arcfile']
                
                #date is simply the topmost dir (YYYYMMDD)
                if int(existing_arcfile.split(os.path.sep)[-2]) > int(new_arcfile.split(os.path.sep)[-2]):
                    skipped_arcfiles.append(new_arcfile)
                    break
            studydata[filemrn]['arcfile']=new_arcfile

sys.stderr.write(str(len(skipped_arcfiles))+" mrn archive duplicates skipped.\n")

#remove MRN if no archive found in previous loop

no_archives_found=[]
for mrn in list(studydata.keys()):
    try:
        studydata[mrn]['arcfile']
    except KeyError: #no file found in previous loop, then we remove the mrn because nothing to study.
        del studydata[mrn]
        no_archives_found.append(mrn)

sys.stderr.write(str(len(no_archives_found))+" mrns did not have a file in the pinnacle archive. Skipping them from study.\n")

#dump the archive to local pinnacle dir

skip_dump=[]
inst_files=[]
for mrn,subdicts in studydata.items():
    #even when skipping dump, stil generating new LPDB file so need to fill inst_files
    inst_files.append(os.path.join(local_pinnacle_dir,str(mrn)+'Institution'))
    if os.path.isfile(os.path.join(local_pinnacle_dir,str(mrn)+'Institution')) and overwrite == False:
        skip_dump.append(mrn)
        #sys.stderr.write("Mrn "+mrn+" already dumped, skipping dump...\n")
        continue
    else:
        filename = subdicts['arcfile']
        sys.stderr.write("Found mrn file "+filename+" in Pinnacle archive, copying...\n")
        #use 7zip because its much faster and autorenames illegal chars (dont worry bout errors)
        if internal_untar is False:
            os.system(zexe+' x '+filename+ ' -so | '+zexe+' x -aoa -si -ttar -o'+local_pinnacle_dir)
        if internal_untar:
            #use python internal untar, no deps but slower.
            with tarfile.open(os.path.join(root, filename),'r') as tarball:
                for f in tarball: #replace invalid chars like tar to underscores
                    f.name = re.sub(r'[:]', '_', f.name)
                tarball.extractall(local_pinnacle_dir)
        #all is extracted in same dir. rescue Institution files because we need them later.
        os.rename(os.path.join(local_pinnacle_dir,'Institution'),os.path.join(local_pinnacle_dir,str(mrn)+'Institution'))

sys.stderr.write(str(len(skip_dump))+" mrn dumps skipped because existing data encountered.\n")

#make lpdb file

with open(lpdbfile, 'w') as dest_file:
    dest_file.write(lpdb_header)
    
    firstFile = True #copy only first Institution file
    lastFile = False
    
    for i,inst_file in enumerate(inst_files):
        if i+1 == len(inst_files):
            lastFile = True
        with open(inst_file,'r',errors='ignore') as inst_file_content:
            writeline = False
            if firstFile:
                writeline = True
            for line in inst_file_content:
                if 'PatientLite ={' in line:
                    writeline=True
                if writeline:
                    dest_file.write(line)
                if writeline==True and '};' in line:
                    writeline=False
                    if firstFile:
                        firstFile = False
                    if lastFile:
                        writeline = True
        #os.remove(inst_file) #leave, is proof of dump for possible next run
    dest_file.write(lpdb_footer)

#update pinnacls_urls to local url and dump to disk for further use

newurls=[]
for mrn,subdicts in studydata.items():
    for upi, urls in subdicts.items():
        if upi == 'arcfile':
            continue
        #loop over urls
        for url in urls:
            new_url = "["+local_pinnacle_dbname+"]"+url.split("]")[-1]
            url=new_url
            newurls.append(new_url+'\n')
            if mrn not in url:
                sys.stderr.write("mrn/upi mismatch: "+mrn+", "+upi+", "+url+"\n")

with open(os.path.join(local_pinnacle_dir,'purls.txt'),'w') as purls:
    purls.writelines(newurls) #doesnt do newlines

end_time = time.time()

sys.stderr.write("Task completed. Total runtime: "+str(end_time-start_time)+"\n")


