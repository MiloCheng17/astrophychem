import os, sys, re
from numpy import *

#def get_opt_info(base_dir):   ### opt output file
#    geom = {}
#    xyz = {}
#    energies = {}
#    outf = base_dir + '/1.out'
#    f = open(outf,'r')
#    lines = f.read()
#    f.close()
#
#    ### read internal coord, bond length in Angstroms ###
#    inter = re.search( r'Optimized variables\n.*?\*', lines, re.DOTALL)
#    c = inter.group().split()[2:-1] ### as string
#    ### ['Optimized', 'variables', 'CUO=', '1.78154347', 'ANGSTROM', 'OH=', '0.96187573', 'ANGSTROM', 'CUOH=', '109.16648709', 'DEGREE', '*'] ###
#    count = int(len(c)/3)
#    for i in range(count):
#        key = c[i*3][:-1]
#        geom[key] = float(c[i*3+1])
#
#    ### cartesian coord ###
#    cart = re.search( r'Current geometry \(xyz format, in Angstrom\)\n.*?\*', lines, re.DOTALL)
#    c = cart.group().split()
#    num_atoms = int(c[6])
#    basis = c[7]
#    E = float(c[8].split('=')[-1])
#    for num in range(num_atoms):
#        key = c[9+num*4]
#        xyz[key] = array([c[10+num*4],c[11+num*4],c[12+num*4]]).astype(float)
#
#    ### energies ###
#    energy = re.search( r'\s+OPTG\(\S+\)\S+.*?\n.*?\*', lines, re.DOTALL)
#    c = energy.group(0).split('\n')[-3:-1]
#    name = c[0].split()
#    val  = c[1].split()
#    num = len(name)
#    for i in range(num):
#        key = name[i]
##        try:
##            energies[key].append(float(val[i]))
##        except:
##            energies[key] = [ float(val[i]) ]
#        energies[key] = float(val[i])
#
#    ### basis_sets info ###
#    base_info = re.search( r'NUMBER OF CONTRACTIONS\:\s+\d+', lines)
#    num_basis = int(base_info.group().split()[-1])
#
#    return geom, xyz, energies, num_basis


#def get_geom_change(base_dir,keys):    # anpass output file
#    anpass = base_dir + '/anpass.out'
#    change_geom = {}
#    f = open(anpass,'r')
#    lines = f.read()
#    f.close()
#
#    ### read internal coord unit in Angstroms ###
#    inter = re.search( r'M I N I M U M\n.*?\n0EIGENVALUE\(S\)', lines, re.DOTALL)
#    c = inter.group(0).split('\n')
#    energy = float(c[2].split()[-1])
#    geom = c[3:-2]
#    for i in range(len(keys)):
#        change_geom[keys[i]] = float(geom[i].split()[-1])
#    return change_geom, energy


def get_geom_change(anpass):    # anpass output file
#    anpass = base_dir + '/anpass.out'
    change_geom = [] 
    f = open(anpass,'r')
    lines = f.read()
    f.close()

    ### read internal coord unit in Angstroms ###
    inter = re.search( r'M I N I M U M\n.*?\n0EIGENVALUE\(S\)', lines, re.DOTALL)
    c = inter.group(0).split('\n')
    energy = float(c[2].split()[-1])
    geom = c[3:-2]
    for i in range(len(geom)):
        change_geom.append( float(geom[i].split()[-1]) )
    return change_geom, energy


def get_new_geom(ref_geom,geom_change):  ### order of keys match geom_change
    new_geom = []
    for key in range(len(ref_geom)):
        print ref_geom[key],  geom_change[key]
        new_geom.append( float(ref_geom[key] + geom_change[key]) )
    return new_geom

def get_disp_intdero(base_dir):
    intdero = base_dir + '/intder.out'
    disps = {}
    f = open(intdero,'r')
    lines = f.readlines()
    f.close()

    num_atoms = int(lines[11].split()[0])
    for i in range(len(lines)):
        step = re.search( r'DISPLACEMENT  ',lines[i] )
        if step:
            key = int(lines[i].split()[-1])
            disps[key] = []
            continue
        m = re.search( r'NEW CARTESIAN GEOMETRY \(BOHR\)',lines[i] )
        if m:
            for num in range(num_atoms):
                c = array(lines[i+2+num].split())
                c = map(float,c)
                disps[key].append(c)
            disps[key] = array(disps[key])
            continue
    return disps


def get_disp_file07(base_dir,natoms):
    intdero = base_dir + '/file07'
    f = open(intdero,'r')
    lines = f.readlines()
    f.close()

    disps = {}
    count = 1
    total = len(lines)/(natoms+1)

    for i in range(total):
        key = count + i
        for j in range(natoms):
            c = lines[1+j+i*(natoms+1)].split()
            c = map(float,c)
            try:
                disps[key].append(c)
            except:
                disps[key] = [c]
        disps[key] = array(disps[key])
    return disps


def get_ref_geom(input):  ### order of keys match geom_change, gaussian format internal coord
    #ref_zmat = base_dir + 'ref.int'
    f = open(input,'r')
    lines = f.readlines()
    f.close()

    ref_geom = []
    variables = []
    l = len(lines)
    for i  in range(l):
        if lines[i][2:11] == 'Variables': 
            num = i+1
            break
    for k in range(num,l-1):
        c = lines[k].split()
        print c
        key = c[0]
        variables.append(key)
        ref_geom.append( float(c[1]) )
    return ref_geom, variables

def get_ff(f03):
    dat = genfromtxt(f03,skip_header=1)
    ff = dat[:,-1]
    f = open('force_constants','w')
    for i in range(dat.shape[0]):
        name = 'F$_{'
        for j in range(4):
            if dat[i,j] != 0:
                name += str(int(dat[i,j]))
        name += '}$'
        if len(name) > 7:
            f.write('%-12s'%name)
            f.write('%10.5f\n'%ff[i])
            print '%6d%5d%5d%5d%20.12f'%(dat[i,0],dat[i,1],dat[i,2],dat[i,3],dat[i,4])
    f.close()
        

