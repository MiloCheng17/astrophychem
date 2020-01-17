import os, sys, re
from numpy import *
from io import IOBase


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
            print(__name__ + " Error: cannot read " + spectrof)
            sys.exit() 

        llines = len(lines)
        num_taup = []
        num_de = 0
        num_he = 0
        num_dtj = 0
        num_dj = 0
        num_hj = 0
        num_be = 0
        num_bs = []
        num_coord = 0
        num_int = []
        num_freq = 0
        num_eig = 0

        nbond  = int(lines[14].split()[2])
        nbend  = int(lines[15].split()[2])
        nlbend = int(lines[16].split()[2])
        nofpb  = int(lines[17].split()[2])
        ntors  = int(lines[18].split()[2])
        
        for i in range(llines):
            if lines[i][-4:-1] == 'BZS':                     # Bs, B0
                num_bs.append( [i + 1, i - 7] )
        
        regex = re.compile('\s+\( [0-9]\)')
        for line in lines:
            if regex.search(line):
                num_int.append(lines.index(line))
            if line[1:5] == 'TAUP':
                num_taup.append(lines.index(line))
                continue
            if line[1:4] == 'De ':
                num_de = lines.index(line)
                continue
            if line[1:4] == 'He ':
                num_he = lines.index(line)
                continue
            if 'DELTA J ' in line:                # Constants in the A reduced Hamiltonian
                num_dtj = lines.index(line)
                continue
            if line[2:6] == 'D J ':                      # Constants in the S reduced Hamiltonian D J
                num_dj = lines.index(line)
                continue
            if line[2:6] == 'H J ':                      # Constants in the S reduced Hamiltonian H D J
                num_hj = lines.index(line)
                continue
            if 'BAND CENTER ANALYSIS' in line:           # harmonic and fundamental frequencies
                num_freq = lines.index(line)+4
                continue
            if 'EIGENVALUES AND EIGENVECTORS' in line:   # eigen values
                num_eig = lines.index(line)+3
                continue
            if line[:23] == 'ROTATIONAL CONSTANTS IN':   # Be
                num_be = lines.index(line) + 2
                continue
#            if line[-4:-1] == 'BZS':                     # Bs, B0
#                num_bs.append(int(lines.index(line) + 1))
#                continue
            if line[:42] == '        VIBRATIONALLY AVERAGED COORDINATES':
                num_coord = lines.index(line) + 8
                break

        ### Internal Coordinates ###
        int_coord = {}
        keys = []
        for i in num_int:
            if 'BOND' in lines[i]:
                key = ('r', '('+lines[i][61:63].strip()+'-'+lines[i][71:73].strip()+')'+'/\AA')
                int_coord[key] = float(lines[i][40:59])
                keys.append(key)
            if 'ANGLE' in lines[i]:
                key = ('\\theta', '('+lines[i][61:63].strip()+'-'+lines[i][71:73].strip()+'-'+lines[i][81:83].strip()+')'+'/\degree')
                int_coord[key] = float(lines[i][40:59])
                keys.append(key)
            if 'TORSION' in lines[i]:
                key = ('\Tau', '('+lines[i][61:63].strip()+'-'+lines[i][71:73].strip()+'-'+lines[i][81:83].strip()+')'+lines[i][91:93].strip()+')'+'/\degree')
                int_coord[key] = float(lines[i][40:59])
                keys.append(key) 


        ### Quartic centrifugal distortion constants TAU ###
        taup = {}
        for i in num_taup:
            c = lines[i].split()
            key = '$\\'+c[0]+'_{'+c[1]+'}$'
            taup[key] = list(map(float,c[2:4]))

        if num_de != 0:
            de = list(map(float,lines[num_de].split()[1:3]))
        else:
            print(" Cannot find De in " + spectrof)
            de = 'None'

        if num_he != 0:
            he = list(map(str,lines[num_he].split()[1:3]))	# in case there is *** in line ##
        else:
            print(" Cannot find He in " + spectrof)
            he = 'None'

        ### Constants in A-reduced Hamiltonian DELTA J ###
        if num_dtj != 0:
            dtj = {}
            for plus in range(20):
                c = lines[num_dtj+plus].split()
                if len(c) == 0: break
                key = c[0]+c[1]
                dtj[key] = list(map(float,c[-2:]))
        else:
            print(spectrof + " Cannot find Constants in A-reduced Hamiltonian DELTA J!")
            dtj = 'None'
        
        ### Constants in S-reduced Hamiltonian DJ ###
        if num_dj != 0:
            dj = {}
            for plus in range(20):
                c = lines[num_dj+plus].split()
                if len(c) == 0: break
                key = c[0]+c[1]
                dj[key] = list(map(float,c[-2:]))
        else:
            print(spectrof + " Cannot find Constants in S-reduced Hamiltonian DJ!")
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
            print(spectrof + " Cannot find Constants in S-reduced Hamiltonian HJ!")
            hj = 'None'

        ### Harmonic and Fundamental frequencies ###
        if num_freq != 0:
            freqs = {}
            for plus in range(20):
                if lines[num_freq+plus] != '\n':
                    c = lines[num_freq+plus].split()
                    if c[0][0] in ['1','2','3','4','5','6','7','8','9'] and len(c) < 5:
                        freqs[c[0]] = [float(c[1]),float(c[2]),float(c[3])]
        else:
            print(spectrof + " Cannot find harmonic and fundamental frequencies!")
            freqs = 'None'

        ### Eigenvalues ###
        if num_eig != 0 and "**" not in lines[num_eig]:
            eigen_val = map(str,lines[num_eig].split())
   #     if num_eig != 0:
   # 	    if "**" not in lines[num_eig]:
   #             eigen_val = map(float,lines[num_eig].split())
   #         else:
   #             eigen_val = map(str,lines[num_eig].split()) # in case there is *** in line ##
        else:
            print(spectrof + " Cannot find Eigen values!")
            eigen_val = 'None'


        ### Equilibrium rotational constants in order of A B C ###
        if num_be != 0:
            be_const = {} 
            be_const['cm$^{-1}$'] = list(map(float,lines[num_be].split()))
            be_const['MHz']  = list(map(float,lines[num_be+1].split()[1::3]))   
        else:
            print(spectrof + " Cannot find Equilibrium rotational constants Be!")
            be_const = 'None'
        
        ### S-reduced rotational constants in order of B C A###
        if num_bs != []:
            bs_const = []
            states = []
            for l in range(len(num_bs)):
                 const_change = list(map(float, lines[num_bs[l][0]].split()))
                 bs_const.append([const_change[2],const_change[0],const_change[1]])
                 states.append(lines[num_bs[l][1]].split()[2:])
    
#                const_change = map(float, lines[num_bs[l][0]].split())
#                bs_const_change = [const_change[2],const_change[0],const_change[1]]
#                states.append(lines[num_bs[l][1]].split()[2:])
##                bs_const.append(bs_const_change)
##            ### in which order xyz abc????
#                lbs = []
#                for change in range(len(bs_const_change)):
#                    lbs.append(bs_const_change[change] + be_const['cm$^{-1}$'][change])               # Bs[:] in cm-1
#                bs_const.append(lbs)               # Bs[:] in cm-1
        else:
            print(spectrof + " Cannot find Equilibrium rotational constants Bs!")
            bs_const = be_const['cm$^{-1}$']

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
#		print c, c[0], len(c)
#                vib_state[key].append(map(float, c[-3:]))   # [Requil, Rg, Ralpha]
                try:
	                vib_state[key].append(list(map(float, c[-3:])))   # [Requil, Rg, Ralpha]
                except:
                    vib_state[key].append(list(map(str, c[-3:])))	# in case there is *** in line ##
        
        self.data = {'taup': taup, 'De': de, 'He': he, 'vib_state': vib_state, 'Be': be_const, 'Bs': bs_const, 'states': states, 'DTJ':dtj, 'DJ': dj, 'HJ': hj, 'int_keys': keys, 'int': int_coord,'freqs': freqs, 'eig': eigen_val}

############### Write File ####################
    def write(self,outf):
        if ( isinstance(outf,IOBase) ):
            f = outf
        else:
            try:
                f = open(outf, 'w')
            except:
                print(__name__ + " Error: failed to write " + outf)
                return False

        vib = self.data['vib_state']
        be  = self.data['Be']
        bs  = self.data['Bs']
        dtj = self.data['DTJ']
        dj  = self.data['DJ']
        hj  = self.data['HJ']
        de  = self.data['De']
        he  = self.data['He']
        tp  = self.data['taup']
        states = self.data['states']
        keys = self.data['int_keys']
        int_coord = self.data['int']
        freqs = self.data['freqs']
        eigen_val = self.data['eig']

#        f.write('Equilibrium Structure\n')
        for key in keys:
            name = '$%s_e$%s'%(key[0],key[1])
            f.write('%-30s %8s %20.4f\n'%(name,'&',int_coord[key]))

        abc = ['$A','$B','$C']
        if be != 'None':
            key = 'MHz'
            #key = 'cm$^{-1}$'
            for i in range(3):
                abc_name=abc[i]+'_e$/'+key
                f.write('%-30s %8s %20.5f\n'%(abc_name,'&',be[key][i]))
            key = 'cm$^{-1}$'
            for i in range(3):
                abc_name=abc[i]+'_e$/'+key
                f.write('%-30s %8s %20.5f\n'%(abc_name,'&',be[key][i]))

        if dj != 'None':
            for key in sorted(dj.keys()):
                #name = key+'/kHz'
                #f.write('%-30s %8s %20.4f'%(name,'&',float(dj[key][1])*1000))
                name = '$'+key+'$'+'/MHz'
                f.write('%-30s %8s %20.7f'%(name,'&',float(dj[key][1])))
                f.write('\n')

        if dtj != 'None':
            for key in sorted(dtj.keys()):
                #name = key+'/kHz'
                #f.write('%-30s %8s %20.4f'%(name,'&',float(dtj[key][1])*1000))
                name = '$'+key+'$'+'/MHz'
                f.write('%-30s %8s %20.7f'%(name,'&',float(dtj[key][1])))
                f.write('\n')

        f.write('\n')    

        if hj != 'None':
            for key in sorted(hj.keys()):
                #name = key+'/Hz'
                #f.write('%-30s %8s %20.7f\n'%(name,'&',float(hj[key][1])))
                name = '$'+key+'$'+'/Hz'
                f.write('%-30s %8s %20.7f\n'%(name,'&',float(hj[key][1])))
        f.write('\n')

        if de != 'None':
            f.write('%-30s %8s %20.7f\n'%('$D_e$/MHz','&',float(de[1])))
        f.write('\n')
        if he != 'None':
            try:
                f.write('%-30s %8s %20.7f\n'%('$H_e$/Hz','&',float(he[1])))
            except:
                f.write('%-30s %8s %20s\n'%('$H_e$/Hz','&',he[1]))
        f.write('\n')
    
    
        if freqs != 'None':
            for key in freqs.keys():
                f.write('%-30s %8s %20.1f\n'%('$\omega_'+key+'$'+'/cm$^{-1}$','&',freqs[key][0]))
        f.write("\n")

        for key_vib in sorted(vib.keys()):
            if key_vib[1] == '0' and key_vib[2] == '0' and key_vib[3] == '0':
                for k in range(len(keys)):
                    key = keys[k]
                    name = '$%s_g$%s'%(key[0],key[1])
                    try:
                        f.write('%-30s %8s %20.4f\n'%(name,'&',vib[key_vib][k][-2]))
                    except:
                        f.write('%-30s %8s %20s\n'%(name,'&',vib[key_vib][k][-2]))
                for k in range(len(keys)):
                    key = keys[k]
                    name = '$%s_z$%s'%(key[0],key[1])
                    try:
                        f.write('%-30s %8s %20.4f\n'%(name,'&',vib[key_vib][k][-1]))
                    except:
                        f.write('%-30s %8s %20s\n'%(name,'&',vib[key_vib][k][-2]))
        f.write('\n')

        if bs != []:
            #f.write('%-20s'%('B0/'+'cm$^{-1}$'))
            for p in range(len(bs)):
                j = bs[p]
                for i in range(3):
                    name = abc[i]+'_%s$/cm$^{-1}$'%p
                    f.write('%-30s %8s %20.5f\n'%(name,'&',j[i]))

    
        if freqs != 'None':
            for key in freqs.keys():
                f.write('%-30s %8s %20.1f\n'%('$\\nv_'+key+'$'+'/cm$^{-1}$','&',freqs[key][1]))
    
        f.close()

            
cuoh = spectro('spectro2.out')
name = sys.argv[1]+'.spectroinfo'
cuoh.write(name)
