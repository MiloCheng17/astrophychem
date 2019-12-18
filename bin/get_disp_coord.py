from numpy import *
import os, sys, re
from mathlib import *

def get_disp_xyz(dispf,natom):
    with open(dispf) as f:
        lines = f.readlines()
    
    nline = len(lines)
    disp = int(nline/(natom+1))
    dict_disp = {}
    
    for i in range(disp):
        dict_disp[i] = []
        for j in range(1,natom+1):
            v = list(map(float,lines[i*(natom+1)+j].split()))
            dict_disp[i].append(v)
        dict_disp[i] = array(dict_disp[i])
    return dict_disp

def get_ref_geom(inp):  ### order of keys match geom_change, gaussian format internal coord
    f = open(inp,'r')
    lines = f.readlines()
    f.close()

    ref_geom = []
    variables = []
    orders = {}
    l = len(lines)
    for i  in range(l):
        if 'Variables' in lines[i]: 
            num = i+1
            break
    for k in range(num,l-1):
        c = lines[k].split()
        key = c[0]
        variables.append(key)
        ref_geom.append( float(c[1]) )
    for k in range(9,num-1):
        c = lines[k].split()
        if len(c) == 3:
            if c[-1] in variables:
                idx = variables.index(c[-1])
                orders[idx] = [k-7,int(c[-2])]
        if len(c) == 5:
            if c[2] in variables:
                idx = variables.index(c[2])
                orders[idx] = [k-7,int(c[1])]
            if c[-1] in variables:
                idx = variables.index(c[-1])
                orders[idx] = [k-7,int(c[1]),int(c[-2])]
        if len(c) == 7:
            if c[2] in variables:
                idx = variables.index(c[2])
                orders[idx] = [k-7,int(c[1])]
            if c[4] in variables:
                idx = variables.index(c[4])
                orders[idx] = [k-7,int(c[1]),int(c[3])]
            if c[6] in variables:
                idx = variables.index(c[6])
                orders[idx] = [k-7,int(c[1]),int(c[3]),int(c[5])]
    return ref_geom, variables, orders


natom = int(sys.argv[1])
dict_disp = get_disp_xyz('file07',natom)
ref_geom, keys, orders = get_ref_geom('ref.int')
#print(ref_geom,keys,orders)

dat = {}
for key in sorted(dict_disp.keys()):
#    print(key)
    dat[key] = []
    disp = dict_disp[key]
    for od in sorted(orders.keys()):
#        print(od,orders[od])
        if len(orders[od]) == 2:
            a = disp[orders[od][0]-1]
            b = disp[orders[od][1]-1]
            var = get_dist(a,b,'Bohr')
        if len(orders[od]) == 3:
            a = disp[orders[od][0]-1]
            b = disp[orders[od][1]-1]
            c = disp[orders[od][2]-1]
            var = get_angle(a,b,c,'Bohr')
        change = var - ref_geom[od]
#        print(od,ref_geom[od],var,change)
        dat[key].append(var)
outf = open('disp_energy.dat','w')        
for key in sorted(dat.keys()):
    outf.write('%6d '%key)
    for i in range(len(ref_geom)):
        outf.write('%12.8f '%dat[key][i])
    outf.write('\n')
outf.close()


        
