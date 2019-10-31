import sys, os
from numpy import *

efile = sys.argv[1]
iatom = sys.argv[2]

dat=genfromtxt(efile,skip_header=3,dtype='str')
atoms = iatom.split(',')
bonds  = dat[:,0].astype(float)/0.529177
for i in range(1,dat.shape[1]):
    energy = dat[:,1]
    frun = open('%s%d_run'%(efile,i),'w')
    frun.write('1\n')
    frun.write('title\n')
    frun.write('%d,5,0,0\n'%len(energy))
    #frun.write('%d,6,0,0\n'%len(energy))
    frun.write('%10.8f\n'%median(bonds))
    for j in range(len(bonds)):
        frun.write('%10.8f,'%bonds[j])
        frun.write('%12s'%'-0.')
    #    frun.write('%s\n'%energy[j].split('.')[-1][:-3])
        frun.write('%s\n'%energy[j].split('.')[-1][:])
    
    for atom in atoms:
        frun.write('%s\n'%atom)
    frun.write('end of input')
        
    
    frun.close()
