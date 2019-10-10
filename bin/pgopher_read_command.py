import os, sys, re
from xlrd import *
from numpy import *

loc = ("%s"%sys.argv[1])
wb = open_workbook(loc)
sheet = wb.sheet_by_name("%s"%sys.argv[2])
edata = genfromtxt('/home/qcheng1/git/astrophychem/bin/exp.dat',skip_header=1,dtype=str,usecols=(0,1,2,3,4,5,6,7,8,9))
rot = genfromtxt('/home/qcheng1/git/astrophychem/bin/exp.dat',skip_header=1,usecols=(-2,-1))
match_id = []

################################################################################################
### v= N'Ka'Kc'J'F'- v= N"Ka"Kc"J"F":17
### v_theory:9
### intensity:10
### column 17: ['v=0', '5', '0', '5', '4.5', '1', '-', 'v=0', '4', '0', '4', '3.5', '0']
################################################################################################

#print(sheet.cell_value(2,17).split())
for i in range(sheet.nrows-1):
#    nu_info = sheet.cell_value(i,17).split()
#    print(nu_info)
#    idx = []
#    for i in [1,2,3,8,9,10,4,11,5,12]:
#        idx.append(nu_info.append(i))
    print(sheet.cell_value(2,17))
    idx = sheet.cell_value(i,17)
    print(idx)
    input()
    if (edata == idx).all(axis=1).nonzero()[0].size > 0 and (edata == idx).all(axis=1).any():
        match_id.append([int((edata == idx).all(axis=1).nonzero()[0]),i+1])


print("%6s %6s %3s %3s %3s -> %-3s %-3s %-3s %5s -> %-5s %3s -> %-3s %12s %12s %12s"%("obs","comp","N'","Ka'","Kc'", 'N"','Ka"','Kc"',"J'",'J"',"F'",'F"','nu_obs','nv_comp','nu_diff'))
for i in range(len(match_id)):
    m = match_id[i][0]
    n = match_id[i][1]
    print("%6d %6d %3s %3s %3s -> %-3s %-3s %-3s %5s -> %-5s %3s -> %-3s %12.3f %12.3f %12.3f"%(match_id[i][0]+1,match_id[i][1]+1,edata[m,0],edata[m,1],edata[m,2],edata[m,3],edata[m,4],edata[m,5],edata[m,6],edata[m,7],edata[m,8],edata[m,9],rot[m,0],sheet.cell_value(n,9),rot[m,0]-sheet.cell_value(n,9)))
