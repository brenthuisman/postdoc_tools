#import

def read(filename,headersize=0):
    sourcefile = open(filename,'r')
    newarr=[]
    for line in sourcefile.readlines()[headersize:]:
        try:
            newarr.append([float(x) for x in line.strip('\n').replace('--','0').replace(',','.').split()])
        except ValueError:
            newarr.append([x for x in line.strip('\n').replace('--','0').replace(',','.').split()])
    sourcefile.close()
    return newarr

def write(oldarr,filename):
    destfile = open(filename,'w')
    for i in range(len(oldarr)):
        for j in range(len(oldarr[i])-1):
            destfile.write(str(oldarr[i][j])+'\t')
        j=j+1
        destfile.write(str(oldarr[i][j])+'\n')
    destfile.close()
    
def print2d(arr):
    ## only works for 2d arrays, eg list of lists.
    ## might be replaced with:
    ## import pandas
    ## pandas.DataFrame(data, teams_list, teams_list)
    for item in arr:
        print(item[0], '\t', '\t'.join(map(str, item[1:])))
    
