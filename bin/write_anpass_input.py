from numpy import *
import os, sys, re
from File_info import *

if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("Usage: write_anpass_input.py anpass.in/anpass2.in intder.in_dir energy_dir (symmetry)")
        sys.exit()
    anpass_name = sys.argv[1]
    dir = sys.argv[2]
    edir = sys.argv[3]
    name = dir+'/intder.in'
    intderf = open(name,'r')
    lines = intderf.readlines()
    intderf.close()
    variable = lines[1].split()[2]
    for line in lines:
        if line[:4] == 'DISP':
            num = line.split()[-1]
            break
    
    hwdir = os.path.abspath('./').split('/')
    hdir = '/'+hwdir[1]+'/'+hwdir[2]
    lib_dir = '%s/git/astrophychem/lib3'%hdir
    if len(sys.argv) == 4:
        anpass = lib_dir+'/anpass'+num
    elif len(sys.argv) == 5:
        anpass = lib_dir+'/anpass'+num+'_'+sys.argv[-1]
    anpassf = open(anpass,'r')
    lines = anpassf.readlines()
    anpassf.close()
    
    f = open(anpass_name,'w')

    efile = edir+'/energy.dat'
    energy = genfromtxt(efile,usecols=-1,dtype=str)
    print(len(energy))
    if len(energy) != int(num):
        print("Number of displacements doesn't match up with number of energy points!")
        sys.exit()
    else:
        title = input('What is the run titile: ')
        f = open(anpass_name,'w')
        f.write('!INPUT\n')
        f.write('TITLE\n')
        f.write('%s\n'%title)
        f.write('INDEPENDENT VARIABLES\n')
        f.write('%s\n'%variable)
        f.write('DATA POINTS\n')
        f.write('%4s   -2\n'%num)
        f.write('(%sF12.8,f20.12)\n'%variable)
        for i in range(len(energy)):
            c = lines[i].split()
            for j in range(len(c)-1):
                f.write('%12s'%c[j])
            #f.write('%20.16f\n'%energy[i])
            f.write('%20s\n'%str(energy[i]))
    for l in range(len(energy),len(lines)):
        f.write(lines[l])
    if anpass_name == 'anpass.in':
        f.write('END OF DATA\n')
        f.write('!FIT\n')
        f.write('!STATIONARY POINT\n')
        f.write('!END')
    if anpass_name == 'anpass2.in':
        ## need to read in anpass out#
        geom_change, energy = get_geom_change(edir)
        print(energy)
        f.write('STATIONARY POINT\n')
        for cgeom in range(len(geom_change)):
            f.write('%20.12f'%geom_change[cgeom])
        f.write('%25.12f\n'%energy)
        f.write('END OF DATA\n')
        f.write('!FIT\n')
        f.write('!END')
    f.close()
