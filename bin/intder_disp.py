import os, sys, re
from numpy import *

step = int(sys.argv[1])
with open('intder.out') as f:
    lines = f.readlines()

dline = []
for i in range(len(lines)):
    if "DISPLACEMENTS" in lines[i]:
        dline.append(i+2)

disp = zeros((len(dline),step))
for s in range(len(dline)):
    i = dline[s]
    key = int(lines[i-4].split()[1])
    if len(lines[i].strip()) == 0 and len(lines[i+1].strip()) == 0:
        continue    
    else:
        for j in range(step):
            if len(lines[i+j].strip()) != 0:
                v = lines[i+j].split()
                disp[s,int(v[0])-1] = float(v[1])
            else:
                break

fout = open('disp.out','w')
for i in range(len(dline)):
    fout.write('%5d'%int(i+1))
    for j in range(step):
        fout.write('%12.8f'%disp[i,j])
    fout.write('\n')
fout.close()

