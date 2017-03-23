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
            sys.exit() 

        llines = len(lines)
        num_taup = []
        num_de = 0
        num_he = 0
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
            if line[1:5] == 'TAUP':
                num_taup.append(lines.index(line))
                continue
            if line[1:4] == 'De ':
                num_de = lines.index(line)
                continue
            if line[1:4] == 'He ':
                num_he = lines.index(line)
                continue
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

        ### Quartic centrifugal distortion constants TAU ###
        taup = {}
        for i in num_taup:
            c = lines[i].split()
            key = c[0]+c[1]
            taup[key] = map(float,c[2:4])

        if num_de != 0:
            de = map(float,lines[num_de].split()[1:3])
        else:
            print " Error: cannot find De in " + spectrof
            de = 'None'

        if num_he != 0:
            he = map(float,lines[num_he].split()[1:3])
        else:
            print " Error: cannot find He in " + spectrof
            he = 'None'

        ### Constants in S-reduced Hamiltonian DJ ###
        if num_dj != 0:
            dj = {}
            for plus in range(20):
                c = lines[num_dj+plus].split()
                if len(c) == 0: break
                key = c[0]+c[1]
                dj[key] = map(float,c[-2:])
        else:
            print spectrof + " Error: cannot find Constants in S-reduced Hamiltonian DJ!"
            dj = 'None'
        
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
            print spectrof + " Error: cannot find Constants in S-reduced Hamiltonian HJ!"
            hj = 'None'
        ### Equilibrium rotational constants ###
        if num_be != 0:
            be_const = {} 
            be_const['cm-1'] = map(float,lines[num_be].split())
            be_const['MHz']  = map(float,lines[num_be+1].split()[1::3])   
        else:
            print spectrof + " Error: cannot find Equilibrium rotational constants Be!"
            be_const = 'None'
        
        ### S-reduced rotational constants ###
        if num_bs != 0:
            bs_const = []
            bs_const_change = map(float, lines[num_bs].split())
            ### in which order xyz abc????
            for change in range(len(bs_const_change)):
                bs_const.append(bs_const_change[change] + be_const['cm-1'][change])               # Bs[:] in cm-1
        else:
            print spectrof + " Error: cannot find Equilibrium rotational constants Bs!"
            bs_const = be_const['cm-1']

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
            key = ()
            for n in range(20):
                if ':' in lines[st[num]+n]:
                    c = lines[st[num]+n].split(':')
                    key += tuple(c[0].split())
                    key += tuple(c[-1].split())
#            key = tuple(lines[st[num]].split(':')[-1].split())  # key is tuple ('0','0','0')
                else:
                    break
            vib_state[key] = []
            for j in range(st[num]+n+3,ed[num]):
                c = lines[j].split()
                vib_state[key].append(map(float, c[-3:]))   # [Requil, Rg, Ralpha]
        
        self.data = {'taup': taup, 'De': de, 'He': he, 'vib_state': vib_state, 'Be': be_const, 'Bs': bs_const, 'DJ': dj, 'HJ': hj}



    def write(self,outf):
        if ( isinstance(outf,file) ):
            f = outf
        else:
            try:
                f = open(outf, 'w')
            except:
                print __name__ + " Error: failed to write " + outf
                return False

        vib = self.data['vib_state']
        be  = self.data['Be']
        bs  = self.data['Bs']
        dj  = self.data['DJ']
        hj  = self.data['HJ']
        de  = self.data['De']
        he  = self.data['He']
        tp  = self.data['taup']
        
        if be != 'None':
            for key in be.keys():
                f.write('%-20s'%('Be/'+key))
                for i in be[key]:
                    f.write('%20.5f'%i)
                f.write('\n')
        else:
            f.write('%-20s%20s'%('Be',be))
            

        if bs != 'None':
            f.write('%-20s'%('B0/'+'cm-1'))
            for i in bs:
                f.write('%20.5f'%i)
            f.write('\n')
        else:
            f.write('%-20s%20s'%('B0',bs))

        if dj != 'None':
            for key in sorted(dj.keys()):
                f.write('%-20s'%(key+'/cm-1'))
                f.write('%20.5e'%dj[key][0])
                f.write('            ')
                f.write('%-20s'%(key+'/MHz'))
                f.write('%20.5f'%dj[key][1])
                f.write('\n')
        else:
            f.write('%-20s%20s\n'%('DJ',dj))

        if hj != 'None':
            for key in sorted(hj.keys()):
                f.write('%-20s'%(key+'/cm-1'))
                f.write('%20.5e'%hj[key][0])
                f.write('            ')
                f.write('%-20s'%(key+'/kHz'))
                f.write('%20.5f'%float(hj[key][1]/1000))
                f.write('\n')
        else:
            f.write('%-20s%20s\n'%('HJ',hj))

        if de != 'None':
            f.write('%-20s'%('De'+'/cm-1'))
            f.write('%20.5e'%de[0])
            f.write('            ')
            f.write('%-20s'%('De'+'/MHz'))
            f.write('%20.5f'%de[1])
            f.write('\n')
        else:
            f.write('%-20s%20s\n'%('De','None'))

        if he != 'None':
            f.write('%-20s'%('He'+'/cm-1'))
            f.write('%20.5e'%he[0])
            f.write('            ')
            f.write('%-20s'%('He'+'/kHz'))
            f.write('%20.5f'%float(he[1]/1000))
            f.write('\n')
        else:
            f.write('%-20s%20s\n'%('He','None'))

        for key in sorted(tp.keys()):
            f.write('%-20s'%(key+'/cm-1'))
            f.write('%20.5e'%tp[key][0])
            f.write('            ')
            f.write('%-20s'%(key+'/MHz'))
            f.write('%20.5f'%tp[key][1])
            f.write('\n')

        for key in sorted(vib.keys()):
            for i in key:
                f.write('%-8s'%i)
            f.write('\n')
            for j in range(len(vib[key])):
                for k in range(3):
                    f.write('%20.6f'%vib[key][j][k])
                f.write('\n')

        f.close()

            
