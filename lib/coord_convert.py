import os, sys, re
from numpy import *

def run_system(cmd):
    print cmd
    os.system(cmd)

def inter_cart(dummy,input,output,geom,variables):
    try:
        f = open(dummy,'r')
        lines = f.readlines()
        f.close()
    except:
        print "Error: cannot read " + dummy
        sys.exit()

    l = len(lines)
    for i  in range(l):
        if lines[i][0] == '0':
            num1 = i+1
            continue
        if lines[i][2:11] == 'Variables': 
            num = i+1
            break
    atoms = []
    f = open(input,'w')
    for i in range(num1):
        f.write(lines[i])
    for i in range(num1,num):
        f.write(lines[i])
        atoms.append(lines[i].split()[0])
    for k in range(num,l-1):
        c = lines[k].split()
        key = c[0]
        idx = variables.index(key)
        f.write('%s %9.8f\n'%(key,geom[idx]))
    f.write(lines[l-1])
    f.close()
    run_system('g09.profile')
    cmd = 'newzmat -izmat -ocart ' + input + ' ' + output
    run_system(cmd)
    

def angstrom_bohr(input,output):
    f = open(input,'r')
    lines = f.readlines()
    f.close()
    f = open(output,'w')
    for n in range(len(lines)):
        c = lines[n].split()
        f.write('%2s'%c[0])
        for m in range(1,4):
            f.write('%17.12f'%(float(c[m])/0.52917721092))
        f.write('\n')
    f.close()

def gangstrom_bohr(input,output):
    f = open(input,'r')
    lines = f.read()
    f.close()
    m = re.search( r'0,1\n.*?1 2',lines,re.DOTALL)
    coord = m.group(0).split('\n')[1:-2]
    f = open(output,'w')
    for i in coord:
        c = i.split()
        f.write('%2s'%c[0])
        for m in range(1,4):
            f.write('%20.10f'%(float(c[m])/0.52917721092))
        f.write('\n')
    f.close()        
