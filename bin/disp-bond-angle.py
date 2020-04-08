import os, sys, re
from numpy import *
from mathlib import *

### Usage: python3 disp-bond-angle.py atom_number Bohr/Ang ###
### change the format for output data file in the end      ### 
### After generate the data file, add energy column to it  ###

atom = int(sys.argv[1])
unit = sys.argv[2]
stre = []
bend = []
tors = []
#########   Read intder.in   ########
with open('intder.in') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if "STRE" in lines[i]:
        v = lines[i].split()
        stre.append([int(v[1])-1,int(v[2])-1])
    if "BEND" in lines[i]:
        v = lines[i].split()
        bend.append([int(v[1])-1,int(v[2])-1,int(v[3])-1])
    if "TORS" in lines[i] or 'OUT' in lines[i]:
        v = lines[i].split()
        tors.append([int(v[1])-1,int(v[2])-1,int(v[3])-1,int(v[4])-1])
    if "DISP" in lines[i]:
        idx_atom = i
        break
xyz = []
for i in range(i-atom,i):
    a = list(map(float,lines[i].split()))
    xyz.append(a)
xyz = array(xyz)

ref_geom = []
for bond in stre:
    ref_geom.append(get_dist(xyz[bond[0]],xyz[bond[1]],unit))
for ang in bend:
    ref_geom.append(get_angle(xyz[ang[0]],xyz[ang[1]],xyz[ang[2]],unit))
for tor in tors:
    ref_geom.append(get_dihedral(xyz[tor[0]],xyz[tor[1]],xyz[tor[2]],xyz[tor[3]],unit))
print(ref_geom)

#########   Read file07   #######
with open('file07') as f:
    lines = f.readlines()

disp_k = 0
disp = {}
for i in range(len(lines)):
    if "GEOMUP" in lines[i]:
        disp_k += 1
        disp[disp_k] = []
        for j in range(i+1,i+1+atom):
            disp[disp_k].append(list(map(float,lines[j].split())))
        disp[disp_k] = array(disp[disp_k])

disp_geom = {}
diff_geom = []
for key in sorted(disp.keys()):
    disp_geom[key] = []
    for bond in stre:
        disp_geom[key].append(get_dist(disp[key][bond[0]],disp[key][bond[1]],unit))
    for ang in bend:
        disp_geom[key].append(get_angle(disp[key][ang[0]],disp[key][ang[1]],disp[key][ang[2]],unit))
    for tor in tors:
        disp_geom[key].append(get_dihedral(disp[key][tor[0]],disp[key][tor[1]],disp[key][tor[2]],disp[key][tor[3]],unit))
    diff_geom.append(array(disp_geom[key]) - array(ref_geom))

f = open('geom_change.dat','w')
#f = open('geom_abs.dat','w')
for i in range(len(diff_geom)):
    for j in range(len(ref_geom)):
        f.write("%20.12f"%diff_geom[i][j])
        #f.write("%20.12f"%disp_geom[i+1][j])
    f.write('\n')
f.close()
    
