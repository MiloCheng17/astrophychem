import os, sys, re
from numpy import *


class spectro:
    """
    information extract from spectro.out
    """

    def __init__(self,spectrof=None):
        if ( spectrof ):
            self.read( spectrof )

    def read(self,spectrof):
        try:
            f = open(spectrof,'r')
            lines = f.readlines()
            f.close()
        except:
            print __name__ + " Error: cannot read " + spectrof
            raise

        llines = len(lines)
        num_dj = 0
        num_hj = 0
        num_be = 0
        num_bs = 0
        num_coord = 0

        nbond  = int(lines[14].split()[2])
        nbend  = int(lines[15].split()[2])
        nlbend = int(lines[16].split()[2])
        nofpb  = int(lines[17].split()[2])
        ntors  = int(lines[18].split()[2])
        
        for line in lines:
            if line[2:6] == 'D J ':                      # Reduced H
                num_dj = lines.index(line)
                continue
            if line[2:6] == 'H J ':                      # H D J
                num_hj = lines.index(line)
                continue
            if line[:23] == 'ROTATIONAL CONSTANTS IN':   # Be
                num_be = lines.index(line) + 2
                continue
            if line[-4:-1] == 'BZS':                     # Bs, B0
                num_bs = lines.index(line) + 1
                continue
            if line[:42] == '        VIBRATIONALLY AVERAGED COORDINATES':
                num_coord = lines.index(line) + 8
                break
        
        ### Constants in S-reduced Hamiltonian DJ ###
        if num_dj != 0:
            dj = {}
            for plus in range(20):
                c = lines[num_dj+plus].split()
                if len(c) == 0: break
                key = c[0]+c[1]
                dj[key] = map(float,c[-2:])
        else:
            print "Error: cannot find Constants in S-reduced Hamiltonian DJ!"
            raise
        
        ### Constants in S-reduced Hamiltonian HJ ###
        if num_hj != 0:
            hj = {}
            for plus in range(20):
                c = lines[num_hj+plus].split()
                if len(c) == 0: break
                key = c[0]+c[1]
                hj[key] = []
                for cd in c[-2:]:
                    cd = cd.replace("D","E")
                    hj[key].append(float(cd))
        else:
            print "Error: cannot find Constants in S-reduced Hamiltonian HJ!"
            raise
        
        ### Equilibrium rotational constants ###
        if num_be != 0:
            be_const = {} 
            be_const['CM-1'] = map(float,lines[num_be].split())
            be_const['MHz']  = map(float,lines[num_be+1].split()[1::3])   
        else:
            print "Error: cannot find Equilibrium rotational constants Be!"
            raise
        
        ### S-reduced rotational constants ###
        if num_bs != 0:
            bs_const = map(float, lines[num_bs].split())                # Bs[:] in CM-1
        else:
            print "Error: cannot find Equilibrium rotational constants Bs!"
            raise

        ### Vibrationally averaged coordinates ###
        vib_state = {}
        num_vib = 0
        st = []
        ed = []
        for i in range(num_coord,llines):
            if lines[i][1:18] == 'VIBRATIONAL STATE':
                num_vib += 1
                st.append(i+1)
                ed.append(i-1)
        ed.append(llines)
        ed.pop(0)
        
        for num in range(num_vib):
            key = tuple(lines[st[num]].split(':')[-1].split())  # key is tuple ('0','0','0')
            vib_state[key] = []
            for j in range(st[num]+4,ed[num]):
                c = lines[j].split()
                vib_state[key].append(map(float, c[2:5]))   # [Requil, Rg, Ralpha]
        
        self.data = {'vib_state': vib_state, 'Be': be_const, 'DJ': dj, 'HJ': hj}
