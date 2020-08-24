import os, sys, re
from numpy import *

#                                                                                                           CuOH    CuCN    TiC2    CuCCH    
#                                                                                                           d   f   d   f   d   f   d   f            
#na = raw_input("Number of atoms:")                                          #1                             3   3   3   3   3   3   4   4   n1   
#ns = raw_input("Number of simple internal coordinates:")                    #2                             3   3   3   3   3   3   7   7   n2
#nsym = raw_input("Number of symmetry internal coordinates:")                #3                             3   0   3   0   3   0   7   0   n3
#nder = raw_input("Highest order of derivative to be transformed:")          #4                             0   4   0   4   0   4   0   4   n4: input intder or freq
#neq = raw_input("If molecule is a stationary point, enter 0.")              #5                             0   0   0   0   0   0   0   0
#nprt = raw_input("Print option, often is 3")                                #6                             3   3   3   3   3   3   3   3   
#ninv = raw_input("Getting initial displacement, type 0, otherwise type 2")  #7                             0   2   0   2   0   2   0   2   n7: input intder or freq
#ndum = raw_input("Number of dummy atoms:")                                  #8                             0   0   1   1   0   0   2   2   n8
#ntest = raw_input("Numerical testing, often 0")                             #9                             0   0   0   0   0   0   0   0
#ngeom = raw_input("Read in Cartesian geom from this file, type 1, other 0") #10                            1   1   1   1   1   1   1   1
#nfreq = raw_input("Perform a frequency analysis in both cart and int, type 3, other 0") #11                0   3   0   3   0   3   0   3   n11: input intder or freq
#irint = raw_input("IR intensity to be computed, often 0")                   #12                            0   0   0   0   0   0   0   0
#nvec = raw_input("Dimension of property, 0 for scalar quantity")            #13                            0   0   0   0   0   0   0   0
#nstop = raw_input("1 to stop after froming 4 matrices")                     #14                            1   0   1   0   1   0   1   0   n14: input intder or freq
#ndisp = raw_input("1 to converge on new cart using first order info")       #15                            1   0   1   0   1   0   1   0   n15: input intder or freq
#nmode = raw_input("Assing normal modes according to diagonal elements, 0")  #16                            0   0   0   0   0   0   0   0

############################################################################################################################################################
#def get_opt_info(base_dir):
#    geom = {}
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
#    return geom
############################################################################################################################################################

#### force constants for intder_freqs.in 6 digits for second derivative, 4 digits for third ####

def run_system(cmd):
    print(cmd)
    os.system(cmd)

### get anpass.out geom_change ###
def get_geom_change(afile):
    with open(afile,'r') as f:
        af = f.read()
    change_geom = []
    inter = re.search( r'M I N I M U M\n.*?\n0EIGENVALUE\(S\)', af, re.DOTALL)
    c = inter.group(0).split('\n')
    change_geom = array(c[-2].split()[:-1]).astype(float)
    return change_geom

### get intder.in info ###
def get_intder_head(ifile):
    with open(ifile,'r') as f:
        intf = f.readlines()
    line_num = []    
    for i in range(len(intf)):    
        if intf[i].split()[0] in ['STRE','BEND','TORS','OUT ','LIN1','SPF ','LINX','LINY','RCOM']:
            line_num.append(i)
        if 'DISP' in intf[i]:
            break
    return i, intf, line_num[-1]    

if __name__ == '__main__':
    if ( os.path.isfile('intder_template') ):
        fb = open('intder_template','r')
        lines = fb.readlines()
        fb.close()
    else:
        print("Error: failed to read intder_template file, make sure the format is correct")
        sys.exit()

    if len(sys.argv) < 3:
        print("Usage: ./write_intder_input.py outputname ref_geom_dir")
        sys.exit()
    output = sys.argv[1]
    ### for section A ###
#    n1 = int(raw_input("Number of atoms:"))
#    n2 = int(raw_input("Number of simple internal coordinates:"))
#    n3 = int(raw_input("Number of symmetry internal coordinates:"))
#    n8 = int(raw_input("Number of dummy atoms:"))

#    iopt = [n1,n2,n3,0,0,0,0,n8,0,0,0,0,0,0,0,0]
    iopt = [0,0,0,0,0,3,0,0,0,1,0,0,0,0,0,0]

    if output == 'intder.in':
        iopt[3]  = 0
        iopt[6]  = 0
        iopt[10] = 0
        iopt[13] = 1
        iopt[14] = 1
        ### getting the reference geom here, do get internal coord or cartesian coord? ###
        xyz_bohr = genfromtxt(sys.argv[2]+'/ref.xyz.bohr',usecols=(1,2,3))

    elif output == 'intder_geom.in':    
        change_geom = get_geom_change('anpass.out')
        iline, intderf, gl_num = get_intder_head('intder.in')
        outf = open(output,'w')    
        for i in range(iline):
            outf.write(intderf[i])
        outf.write('DISP   1\n')
        for j in range(len(change_geom)):
            outf.write('%5d      %13.10f\n'%(int(j+1),change_geom[j]))
        outf.write('%5d'%0)

    elif output == 'intder_freqs.in':
        iopt[3]  = 4  
        iopt[6]  = 2
        iopt[10] = 3
        iopt[13] = 0
        iopt[14] = 0
        ### getting new geom here ###
#        xyz_bohr = genfromtxt(sys.argv[2]+'/1.inp-cart.bohr',usecols=(1,2,3))
        iline, intderf, gl_num = get_intder_head('intder_geom.in')
        with open('intder_geom.out','r') as f:
            geom_lines = f.readlines()
        length = len(geom_lines)    
        for i in range(length):
            if "NEW CARTESIAN GEOMETRY (BOHR)" in geom_lines[i]:
                xyz_bohr = genfromtxt(sys.argv[2]+'/intder_geom.out',skip_header=i+1)
                break

        n1 = xyz_bohr.shape[0]
        As = input("Is this molecule linear? Yes or No ")
        if As == 'Yes':
            n2 = 3*n1-5
            n8 = int(input("Number of dummy atoms:"))
        else:
            n2 = 3*n1-6
            n8 = 0
        n3 = n2 
#        n8 = int(input("Number of dummy atoms:"))

        iopt[0] = n1
        iopt[1] = n2
        iopt[2] = n3
        iopt[7] = n8
        
        ### for section B ###
        sectb = {}
        keys = []
        for line in lines:
            c = line.split(':')
            if 'None' not in c[1]:
                key = c[0].split()[0]
                keys.append(key)
                sectb[key] = []
                b = c[1].split(',')
                for pair in b:
                    sectb[key].append(pair.split())

        f = open(output,'w')
        f.write('# INTDER ##########################\n')
        for i in iopt:
            f.write("%5s"%i)
        f.write('\n')
        for key in keys:
            l = len(sectb[key])
            for i in range(l):
                f.write('%-5s'%key)
                for j in range(len(sectb[key][0])):
                    f.write('%5s'%sectb[key][i][j])
                f.write('\n')
   #    #####################################
   #    ##     Need to fix      #####
   #    #####################################
        for num in range(1,int(n3)+1):
            f.write('%s'%intderf[gl_num+num])
#            f.write('%5s%4s %14.10f\n'%(num,num,1))
        f.write('%4s\n'%0)

        if n8 == 1 and count_nonzero(xyz_bohr[:,-1]) >= n1-1:
            xyz_bohr = vstack((xyz_bohr,array([0.00,1.90,0.00])))
        elif n8 == 2 and count_nonzero(xyz_bohr[:,-1]) >= n1-1:
            xyz_bohr = vstack((xyz_bohr,array([[1.90,0.00,0.00],[0.00,1.90,0.00]])))
        for i in range(xyz_bohr.shape[0]):
#            f.write('        ')
            for j in range(xyz_bohr.shape[1]):
                f.write('%20.10f'%xyz_bohr[i,j])
            f.write('\n')

        if output == 'intder.in':
            if n1 == 3 and As == 'Yes':     # triatomic linear, 69 displacements
                df = 'DISP69'
            elif n1 == 3 and As == 'No':    # triatomic bend, 129 displacements
                df = 'DISP129'
            elif n1 == 4 and As == 'Yes':   # four atoms linear molecule
                df = 'DISP625'

            fname = '/home/qcheng1/python/lib/'+df
            dispf = open(fname, 'r')
            for line in dispf:
                f.write(line)
            dispf.close()

        if output == 'intder_freqs.in':
            atoms = input('Input atoms with math, put space between two atoms: ')
            for atom in atoms.split():
                f.write('%12s'%atom)
            f.write('\n')
            ffdir = input('Input the directory where file fort.9903 locates: ')
            ffname = ffdir + '/fort.9903'
            ff = open(ffname,'r')
            lines = ff.readlines()
            ff.close()
            count = 2
            for i in range(1,len(lines)):
                c = lines[i].split()
                if c[0] == '3' and c[1] == '3' and c[2] == '0' and c[3] == '0':
                    f3300 = float(c[4])
                if c[0] == '3' and c[1] == '3' and c[2] == '3' and c[3] == '3':
                    f3333 = float(c[4])
                if c[1] == '0': 
                    continue
                if c.count('0') >= count:
                    f.write(lines[i])
                else:
                    count = c.count('0')
                    f.write('%5s\n'%'0')
                    f.write(lines[i])
            f.write('%5s'%'0')

            if As == 'Yes' and n1 == 3:
                print("You may need to modify you intder_freqs.in file, F3344=(F3333+4*F33)/3=%.12f"%((f3333+4*f3300)/3))

        f.close()

    else:
        print("You want to gen 'intder.in' or 'intder_freqs.in'")
        sys.exit()
