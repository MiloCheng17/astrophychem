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
        nbond  = int(lines[14].split()[2])
        nbend  = int(lines[15].split()[2])
        nlbend = int(lines[16].split()[2])
        nofpb  = int(lines[17].split()[2])
        ntors  = int(lines[18].split()[2])
   
 #########   Internal Coordinates  #################################  
 #########   'int_keys': keys, 'int': int_coord, num_int   #########  
        int_coord = {}
        keys = []
        num_int = []
        regex = re.compile('\s+\( [0-9]\)')
        for line in lines:
            if regex.search(line):
                num_int.append(lines.index(line))
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
                key = ('\Tau', '('+lines[i][61:63].strip()+'-'+lines[i][71:73].strip()+'-'+lines[i][81:83].strip()+'-'+lines[i][91:93].strip()+')'+'/\degree')
                int_coord[key] = float(lines[i][40:59])
                keys.append(key) 

 #########   QUARTIC CENTRIFUGAL DISTORTION CONSTANTS TAU PRIME   #########
 #########   'taup': taup (cm-1, MHz)             #########################
        taup = {}
        for i in range(llines):
            if lines[i][1:5] == 'TAUP':
                c = lines[i].split()
                key = '$\\'+c[0]+'_{'+c[1]+'}$'
                taup[key] = list(map(float,c[2:4]))

 #########   For Linear Molecules   ########################################
 #########   'de': de, (cm-1, MHz), 'he': he (cm-1, Hz)   ##################
        de = 'None'
        he = 'None'
        for i in range(llines):
            if lines[i][1:4] == 'De ':
                de = list(map(float,lines[i].split()[1:3]))
            if lines[i][1:4] == 'He ':
                he = list(map(str,lines[i].split()[1:3]))	# in case there is *** in line ##
        if de == 'None':
            print(" Cannot find De in " + spectrof)
        if he == 'None':
            print(" Cannot find He in " + spectrof)


 #########   CONSTANTS IN THE A REDUCED HAMILTONIAN   #####################
 #########   'DTJ':dtj (cm-1, MHz)  (QUARTIC)         #####################
        dtj = {}
        for i in range(llines):
            if 'DELTA' in lines[i][:10] or 'delta' in lines[i][:10]:
                c = lines[i].split()
                key = '$\\'+c[0]+'_{'+c[1]+'}$'
                dtj[key] = list(map(float,c[-2:]))
        if not bool(dtj):
            print(spectrof + " Cannot find Constants in A-reduced Hamiltonian DELTA J!")

 #########   CONSTANTS IN THE S REDUCED HAMILTONIAN   #####################
 #########   'DJ': dj (cm-1, MHz) (QUARTIC)           #####################
        dj = {}
        for i in range(llines):
            if lines[i][2:6] in ['D J ', 'D JK', 'D K ', 'd 1 ', 'd 2 ']:
                c = lines[i].split()
                key = '$'+c[0]+'_{'+c[1]+'}$'
                dj[key] = list(map(float,c[-2:]))
        if not bool(dj):
            print(spectrof + " Cannot find Constants in S-reduced Hamiltonian D J!")

 #########   SEXTIC CENTRIFUGAL DISTORTION CONSTANTS   ####################
 #########   'phi': phi (cm-1, Hz)                #########################
        phi = {}
        for i in range(llines):
            if lines[i][1:6] in ['PHI a','PHI b','PHI c']:
                c = lines[i].split()
                key = '$\\'+c[0]+'_{'+c[1]+'}$'
                phi[key] = []
                for cd in c[-2:]:
                    cd = cd.replace("D","E")
                    phi[key].append(float(cd))
        if not bool(phi):
            print(spectrof + " Cannot find SEXTIC CENTRIFUGAL DISTORTION CONSTANTS PHI aaa!")

 #########   CONSTANTS IN THE A REDUCED HAMILTONIAN   #####################
 #########   'phij':phij (cm-1, Hz)  (SEXTIC)      ########################
        phij = {}
        for i in range(llines):
            if lines[i][2:8] in ['PHI J ','PHI K ','PHI JK','PHI KJ','phi j ','phi jk','phi k ']:
                c = lines[i].split()
                key = '$\\'+c[0]+'_{'+c[1]+'}$'
                phij[key] = []
                for cd in c[-2:]:
                    cd = cd.replace("D","E")
                    phij[key].append(float(cd))
        if not bool(phij):
            print(spectrof + " Cannot find Constants in A-reduced Hamiltonian PHI J!")

 #########   CONSTANTS IN THE S REDUCED HAMILTONIAN   #####################
 #########   'HJ': hj (cm-1, Hz) (SEXTIC)             #####################
        hj = {}
        for i in range(llines):
            if lines[i][2:6] in ['H J ', 'H JK', 'H K ', 'H KJ', 'h 1 ', 'h 2 ', 'h 3 ']:
                c = lines[i].split()
                key = '$'+c[0]+'_{'+c[1]+'}$'
                hj[key] = []
                for cd in c[-2:]:
                    cd = cd.replace("D","E")
                    hj[key].append(float(cd))
        if not bool(hj):
            print(spectrof + " Cannot find Constants in S-reduced Hamiltonian H J!")

 #########   ROTATIONAL CONSTANTS IN CM-1 (MHz)   #########################
 #########   'Be': be_const (cm-1, MHz)           #########################
        be_const = {}
        for i in range(llines):
            if "ROTATIONAL CONSTANTS IN CM-1 (MHz)" in lines[i]:
                value_cm = lines[i+2].split()
                num_be_cm = list(map(float,value_cm))
                num_be_str = [value_cm[0][:6],value_cm[1][:6],value_cm[2][:6]]
                value_mhz = lines[i+3].split()
                num_be_mhz = [float(value_mhz[1]),float(value_mhz[4]),float(value_mhz[7])]
            if "ALPHA FOR PRINCIPAL AXIS" in lines[i]:
                key = lines[i].split()[4]
                val_be = lines[i+1].split()[2][:-1]
                if val_be in num_be_str:
                    idx = num_be_str.index(val_be)
                else:
                    nval_be = round(float(val_be),3)
                    for ss in range(len(num_be_cm)):
                        if nval_be == round(num_be_cm[ss],3):
                            idx = ss
                be_const[key] = [num_be_cm[idx],num_be_mhz[idx]]

 #########   VIBRATIONAL CORRECTIONS TO THE ROTATIONAL CONSTANTS  #########
 #########   'Bs': be_const (corr_cm-1, MHz, abs_cm-1, MHz) B0   ##########
        bs_const = {}
        for i in range(llines):
            if lines[i][33:37] == 'AXIS':
                key = lines[i][38]
                bs_const[key] = list(map(float,lines[i+5].split()[:4]))

 #########   Perturbed Fundamental Frequencies   #########  
 #########   'zpe', state_zpe, num_zpe           #########  
        state_zpe = {}
        for i in range(llines):
            if "STATE NO.     ENERGY (CM-1)" in lines[i]:
                num_zpe = [i+3]
                for j in range(i+3,i+3+1000):
                    if "<>" not in lines[j]:
                        num_zpe.append(j)
                    else:
                        break
        for i in range(num_zpe[0],num_zpe[-1]):
            v = lines[i].split()
            if len(v) >= 8:
                state_zpe[str(int(v[0])-1)] = float(v[2])

                    
 #########   Harmonic and Fundamental Frequencies      #########  
 #########   'freqs':freqs, (harm, fund, diff, cm-1)   #########  
        freqs = {}
        for i in range(llines):
            if 'BAND CENTER ANALYSIS' in lines[i]:
                for plus in range(20):
                    if lines[i+4+plus] != '\n':
                        c = lines[i+4+plus].split()
                        if c[0][0] in ['1','2','3','4','5','6','7','8','9'] and len(c) < 5:
                            freqs[c[0]] = [float(c[1]),float(c[2]),float(c[3])]

 #########   VIBRATIONALLY AVERAGED COORDINATES        #########  
 #########   'vib_state':vib_state, (Re,Rg,Ralpha)     #########  
        vib_state = {}
        num_vib = 0
        st = []
        ed = []
        for i in range(llines):
            if 'VIBRATIONALLY AVERAGED COORDINATES' in lines[i]:
                for j in range(i+8,llines):
                    if lines[j][1:18] == 'VIBRATIONAL STATE':
                        num_vib += 1
                        st.append(j+1)
                        ed.append(j-1)
        ed.append(llines)
        ed.pop(0)
        
        for num in range(num_vib):
            key = ()
            for n in range(20):
                if ':' in lines[st[num]+n]:
                    c = lines[st[num]+n].split(':')
                    key += tuple(c[0].split())
                    key += tuple(c[-1].split())
##            key = tuple(lines[st[num]].split(':')[-1].split())  # key is tuple ('0','0','0')
                else:
                    break
            vib_state[key] = []
            for j in range(st[num]+n+3,ed[num]):
                c = lines[j].split()
##		print c, c[0], len(c)
##                vib_state[key].append(map(float, c[-3:]))   # [Requil, Rg, Ralpha]
                try:
	                vib_state[key].append(list(map(float, c[-3:])))   # [Requil, Rg, Ralpha]
                except:
                    vib_state[key].append(list(map(str, c[-3:])))	# in case there is *** in line ##

 #########   'int_keys': keys, 'int': int_coord, num_int   ################  
 #########   'taup': taup (cm-1, MHz)                      ################
 #########   'De': de, (cm-1, MHz), 'He': he (cm-1, Hz)    ################
 #########   'DTJ':dtj (cm-1, MHz)  (QUARTIC)              ################
 #########   'DJ': dj (cm-1, MHz) (QUARTIC)                ################
 #########   'phi': phi (cm-1, Hz)                         ################
 #########   'phij':phij (cm-1, Hz)  (SEXTIC)              ################
 #########   'HJ': hj (cm-1, Hz) (SEXTIC)                  ################
 #########   'Be': be_const (cm-1, MHz)i                   ################
 #########   'Bs': be_const (corr_cm-1, MHz, abs_cm-1, MHz) B0   ##########
 #########   'zpe', state_zpe, num_zpe                     ################  
 #########   'freqs':freqs, (harm, fund, diff, cm-1)       ################  
 #########   'vib_state':vib_state, (Re,Rg,Ralpha)         ################  
        self.data = {'int_keys':keys, 'int':int_coord, 'taup':taup, 'De':de, 'He':he, 'DTJ':dtj, 'DJ':dj, 'phi':phi, 'phij':phij, 'HJ': hj, 'Be':be_const, 'Bs':bs_const, 'zpe':state_zpe, 'vib_state':vib_state, 'freqs': freqs}

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

        keys = self.data['int_keys']#########   'int_keys': keys, 'int': int_coord, num_int   ################  
        int_coord = self.data['int']
        be  = self.data['Be']       #########   'Be': be_const (cm-1, MHz)i                   ################
        dj  = self.data['DJ']       #########   'DJ': dj (cm-1, MHz) (QUARTIC)                ################
        dtj = self.data['DTJ']      #########   'DTJ':dtj (cm-1, MHz)  (QUARTIC)              ################
        tp  = self.data['taup']     #########   'taup': taup (cm-1, MHz)                      ################
        phi = self.data['phi']      #########   'phi': phi (cm-1, Hz)                         ################
        phij= self.data['phij']     #########   'phij':phij (cm-1, Hz)  (SEXTIC)              ################
        hj  = self.data['HJ']       #########   'HJ': hj (cm-1, Hz) (SEXTIC)                  ################
        de  = self.data['De']       #########   'De': de, (cm-1, MHz), 'He': he (cm-1, Hz)    ################
        he  = self.data['He']
        bs  = self.data['Bs']       #########   'Bs': be_const (corr_cm-1, MHz, abs_cm-1, MHz) B0   ##########
        freqs = self.data['freqs']  #########   'freqs':freqs, (harm, fund, diff, cm-1)       ################  
        vib = self.data['vib_state']#########   'vib_state':vib_state, (Re,Rg,Ralpha)         ################  
        states = self.data['zpe']   #########   'zpe', state_zpe, num_zpe                     ################  

        for key in keys:
            name = '$%s_e$%s'%(key[0],key[1])
            f.write('%-30s %8s %20.4f\n'%(name,'&',int_coord[key]))

 #########   'Be': be_const (cm-1, MHz)                    ################
 #########   'Bs': be_const (corr_cm-1, MHz, abs_cm-1, MHz) B0   ##########
        if be != 'None':
            for akey in be.keys():
                key1 = 'cm$^{-1}$'
                key2 = 'MHz'
                abc_name1 = '$'+akey+'_e$/'+key1
                abc_name2 = '$'+akey+'_e$/'+key2
                f.write('%-30s %8s %20.5f\n'%(abc_name1,'&',be[akey][0]))
                f.write('%-30s %8s %20.5f\n'%(abc_name2,'&',be[akey][1]))

        if dj != 'None':
            for key in sorted(dj.keys()):
                #name = key+'/kHz'
                #f.write('%-30s %8s %20.4f'%(name,'&',float(dj[key][1])*1000))
                name = key+'/MHz'
                f.write('%-30s %8s %20.7f'%(name,'&',float(dj[key][1])))
                f.write('\n')

        if dtj != 'None':
            for key in sorted(dtj.keys()):
                #name = key+'/kHz'
                #f.write('%-30s %8s %20.4f'%(name,'&',float(dtj[key][1])*1000))
                name = key+'/MHz'
                f.write('%-30s %8s %20.7f'%(name,'&',float(dtj[key][1])))
                f.write('\n')
            f.write('\n')    

        if hj != 'None':
            for key in sorted(hj.keys()):
                #name = key+'/Hz'
                #f.write('%-30s %8s %20.7f\n'%(name,'&',float(hj[key][1])))
                name = key+'/Hz'
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
    
        if bs != 'None':
            for akey in be.keys():
                key1 = 'cm$^{-1}$'
                key2 = 'MHz'
                abc_name3 = '$'+akey+'_0$/'+key1
                abc_name4 = '$'+akey+'_0$/'+key2
                f.write('%-30s %8s %20.5f\n'%(abc_name3,'&',bs[akey][2]))
                f.write('%-30s %8s %20.5f\n'%(abc_name4,'&',bs[akey][3]))
    
        if freqs != 'None':
            for key in freqs.keys():
                f.write('%-30s %8s %20.1f\n'%('$\omega_'+key+'$'+'/cm$^{-1}$','&',freqs[key][0]))
        f.write("\n")

        for key_vib in sorted(vib.keys()):
            #if sum(list(map(int,key_vib[1:]))) == 0:
            #if key_vib[1] == '0' and key_vib[2] == '0' and key_vib[3] == '0':
            if sum([int(kb) for kb in key_vib if type(kb)== int or kb.isdigit()]) == 0:
                for k in range(len(vib[key_vib])):
                    key = keys[k]
                    name = '$%s_g$%s'%(key[0],key[1])
                    try:
                        f.write('%-30s %8s %20.4f\n'%(name,'&',vib[key_vib][k][-2]))
                    except:
                        f.write('%-30s %8s %20s\n'%(name,'&',vib[key_vib][k][-2]))
                for k in range(len(vib[key_vib])):
                    key = keys[k]
                    name = '$%s_z$%s'%(key[0],key[1])
                    try:
                        f.write('%-30s %8s %20.4f\n'%(name,'&',vib[key_vib][k][-1]))
                    except:
                        f.write('%-30s %8s %20s\n'%(name,'&',vib[key_vib][k][-2]))
        f.write('\n')

        if freqs != 'None':
            for key in freqs.keys():
                f.write('%-30s %8s %20.1f\n'%('$\\nv_'+key+'$'+'/cm$^{-1}$','&',freqs[key][1]))
        f.write('\n')

        if freqs != 'None':
            for key in freqs.keys():
                f.write('%-30s %8s %20.1f\n'%('$\\nv_'+key+'$'+'/cm$^{-1}$','&',states[key.replace('*','')]))
    
    
        f.close()

            
cuoh = spectro('spectro2.out')
name = sys.argv[1]+'.spectroinfo'
cuoh.write(name)
