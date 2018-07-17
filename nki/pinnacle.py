lpdb_header = """SiteName = "AvL/NKI Amsterdam";
InstitutionList ={
Institution ={
"""
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
"""
#/* 6Ñ */
#"""

def make_lpdb(inst_files,lpdbfile):
	with open(lpdbfile, 'w') as dest_file:
		dest_file.write(lpdb_header)
			
		firstFile = True #copy only first Institution file
		lastFile = False
		
		for i,inst_file in enumerate(inst_files):
			if i+1 == len(inst_files):
				lastFile = True
			with open(inst_file,'r',errors='ignore') as inst_file_content:
				j=1
				writeline = False
				if firstFile:
					writeline = True
				for line in inst_file_content:
					if 'PatientLite ={' in line:
						writeline=True
					if writeline:
						if 'FormattedDescription' in line:
							#should be ten '&' in here, with something after the last '&'
							tenthindex = findnth(line,'&',9) #9 because 0 is first
							if line[tenthindex+1] == '"':
								line = line[:tenthindex] + '2013-05-14 09:24:45";';
						if 'PatientID' in line:
							line = "PatientID = "+str(j)+";\n"
							j+=1
						dest_file.write(line)
					if writeline==True and '};' in line:
						writeline=False
						if firstFile:
							firstFile = False
						if lastFile:
							writeline = True
			#os.remove(inst_file) #dont remove, is proof of dump for possible next run
		dest_file.write(lpdb_footer)

def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)
