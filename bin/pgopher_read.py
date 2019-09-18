import os, sys, re
from xlrd import *
from numpy import *

loc = ("%s"%sys.argv[1])
wb = open_workbook(loc)
#sheet = wb.sheet_by_name("%s"%sys.argv[2])
sheet = wb.sheet_by_name("Final S-reduced")

################################################################################################
### N':23   N":30
### Ka':24  Ka":31
### Kc':25  Kc":32
### J':26   J":33
### F':27   F":34
### v_theory:9
################################################################################################

edata = genfromtxt('exp.dat',skip_header=1,dtype=str,usecols=(0,1,2,3,4,5,6,7,8,9))
rot = genfromtxt('exp.dat',skip_header=1,usecols=(-2,-1))
match_id = []
for i in range(sheet.nrows-1):
    idx = []
    for j in [23,24,25,30,31,32]: #,26,33,27,34]:
        idx.append(str(int(sheet.cell_value(i+1,j))))
    for j in [26,33]:
        idx.append(str(round(sheet.cell_value(i+1,j),1)))
    for j in [27,34]:
        idx.append(str(int(sheet.cell_value(i+1,j))))
    if (edata == idx).all(axis=1).nonzero()[0].size > 0 and (edata == idx).all(axis=1).any():    
#        print( int((edata == idx).all(axis=1).nonzero()[0]) )
        match_id.append([int((edata == idx).all(axis=1).nonzero()[0]),i+1])
#    match_id.append(int( where((edata == idx).all(axis=1))[0] ))    
#    print( where((edata == idx).all(axis=1)) ) 

#print(sheet.cell_value(0,1))
#print(match_id)
print("%3s %3s %3s -> %-3s %-3s %-3s %5s -> %-5s %3s -> %-3s %9s %9s %9s"%("N'","Ka'","Kc'", 'N"','Ka"','Kc"',"J'",'J"',"F'",'F"','v_obs','v_comp','v_diff'))
for i in range(len(match_id)):
    m = match_id[i][0]
    n = match_id[i][1]
    print("%3s %3s %3s -> %-3s %-3s %-3s %5s -> %-5s %3s -> %-3s %9.3f %9.3f %9.3f"%(edata[m,0],edata[m,1],edata[m,2],edata[m,3],edata[m,4],edata[m,5],edata[m,6],edata[m,7],edata[m,8],edata[m,9],rot[m,0],sheet.cell_value(n,9),rot[m,0]-sheet.cell_value(n,9)))
