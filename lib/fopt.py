import sys, os, re
from numpy import *

class fopt:
    """
    information extract from optimization file
    """

    def __init__(self,optfile=None):
        if ( optfile ):
            self.read( optfile )

    def read(self,optfile):
        try:
            f = open(optfile,'r')
            lines = f.read()
            f.close()
        except:
            print __name__ + " Error: cannot read " + optfile
            raise


        vars = []
        zmat = []
        title = None
        natom = 0
        atomlist = []
        xyz  = []
        energies = {}
        nbasis = 0

        ### read internal coord, bond length in Angstroms ###
        inter = re.search( r'Optimized variables\n.*?\*', lines, re.DOTALL)
        c = inter.group().split()[2:-1] ### as string
        ### ['Optimized', 'variables', 'CUO=', '1.78154347', 'ANGSTROM', 'OH=', '0.96187573', 'ANGSTROM', 'CUOH=', '109.16648709', 'DEGREE', '*'] ###
        count = int(len(c)/3)
        for i in range(count):
            key = c[i*3][:-1]
            zmat.append( float(c[i*3+1]) )
            vars.append(key)

        ### cartesian coord ###
        cart = re.search( r'Current geometry \(xyz format, in Angstrom\)\n.*?\*', lines, re.DOTALL)
        c = cart.group().split()
        natom = int(c[6])
        title = c[7]    ### 'UCCSD(T)/AV5Z-DK ###
        E = float(c[8].split('=')[-1])
        for num in range(natom):
            key = c[9+num*4]
            atomlist.append(key)
            xyz.append( [float(c[10+num*4]),float(c[11+num*4]),float(c[12+num*4])] )

        ### energies ###
        energy = re.search( r'\s+OPTG\(\S+\)\S+.*?\n.*?\*', lines, re.DOTALL)
        c = energy.group(0).split('\n')[-3:-1]
        name = c[0].split()
        val  = c[1].split()
        num = len(name)
        for i in range(num):
            key = name[i]
            energies[key] = float(val[i])
    
        ### basis_sets info ###
        base_info = re.search( r'NUMBER OF CONTRACTIONS\:\s+\d+', lines)
        nbasis = int(base_info.group().split()[-1])

        self.data = { 'natom':natom, 'title': title, 'atomlist': atomlist, 'xyz': xyz, 'variables': vars, 'zmat': zmat, 'energies': energies, 'nbasis': nbasis }


    def write(self,outf):
        if ( isinstance(outf,file) ):
            f = outf
        else:
            try:
                f = open(outf, 'w')
            except:
                print __name__ + " Error: failed to write " + outf
                return False
        
        zmat      = self.data['zmat']
        variables = self.data['variables']
        xyz       = self.data['xyz']
        energies  = self.data['energies']
        title     = self.data['title']
        natom     = self.data['natom']
        nbasis    = self.data['nbasis']
        atomlist  = self.data['atomlist']

        f.write('%s\n'%title)
        f.write('Energy')
        for key in energies.keys():
            if 'OPTG' in key:
                f.write( '%12s: %10.5f\n'%(key[5:-1],energies[key]) )
        f.write( '%19s %5d\n'%('num_basis:',nbasis))
        f.write('Internal coordinates:\n')
        for i in range(len(variables)):
            f.write( '%8s %10.5f\n'%(variables[i],zmat[i]) ) 
        f.write('Cartesian coordinates:\n')
        for i in range(len(xyz)):
            f.write('%6s'%atomlist[i])
            for j in range(3):
                f.write('%15.10f'%xyz[i][j])
            f.write('\n')
        f.close()

