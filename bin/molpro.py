#Readinter - Py Version
#mgnn CCSD(T)
import math
import os
import subprocess

#Notes:
#1) file07 is generated from an intder output from a xyz(bohr) geometry and numerical displaces
#2) this file functions based on the modulo operator: every 4th line is hydrogen in file07 for mgnn.
#3) docc/socc is dependent on the variable x which is where the out of plane bend manifests itself in mass weighted displacements through intder, apparently.
#4) line by line strip stores as strings, variables need to be converted to floats for a standard write input explicitly, as done here.
#5) your cropped energies (for anpass) will be named according the mol variable at the end of this script.
#6) Other levels of theory require a change in the grep command at the bottom to properly grab energies (potentially changing the nrg[#] value.

os.mkdir('inp')
file = open('file07')
count=1
disp=0
ws=" "*7
for line in file:
        if "#" in line:
                count+=1
                disp+=1
                print "Displacement",disp
                if disp<10:                                                      
                        os.mkdir ('inp/mgnn00%d/' %disp)
                        f=open('inp/mgnn00%d/1.inp' %disp, 'w')
                elif disp<100:
                        os.mkdir ('inp/mgnn0%d/' %disp)
                        f=open('inp/mgnn0%d/1.inp' %disp, 'w')
                else:
                        os.mkdir ('inp/mgnn%d/' %disp)
                        f=open('inp/mgnn%d/1.inp' %disp, 'w')
                f.write ('***, mgnn QFF SP Energy Calc #%2d\n' %disp)
                f.write ("memory,300,m\n")
                f.write ("\n")
                f.write (" gthresh,energy=1.d-12\n")
                f.write (" print, orbitals,basis\n")
		f.write ("\ngeomtyp=xyz\n")
		f.write ("bohr\n")
#		f.write ("symmetry x\n")
                f.write ("geometry={\n")
		f.write ("3\n")
		f.write ("mgnn\n")
                continue
        else:
                if disp<10:                                                      
                        f=open('inp/mgnn00%d/1.inp' %disp, 'a')
                elif disp<100:
                        f=open('inp/mgnn0%d/1.inp' %disp, 'a')
                else:
                        f=open('inp/mgnn%d/1.inp' %disp, 'a')
                if count%4 == 2:
                        coords = line.strip().split()
                        print "MG",ws,coords[0],ws,coords[1],ws,coords[2]
                        x=float(coords[0])
                        y=float(coords[1])
                        z=float(coords[2])
                        f.write ("MG , %20.12f , %20.12f , %20.12f\n" % (x,y,z))
                        count+=1
                        continue
                elif count%4 == 3:
                        coords = line.strip().split()
                        print "N",ws,coords[0],ws,coords[1],ws,coords[2]
                        x=float(coords[0])
                        y=float(coords[1])
                        z=float(coords[2])
                        f.write (" N , %20.12f , %20.12f , %20.12f\n" % (x,y,z))
                        count+=1
                        continue
                elif count%4 == 0:
                        coords = line.strip().split()
                        print "N",ws,coords[0],ws,coords[1],ws,coords[2]
                        x=float(coords[0])
                        y=float(coords[1])
                        z=float(coords[2])
                        f.write (" N , %20.12f , %20.12f , %20.12f\n" % (x,y,z))
                        count+=1
                f.write (" }\n")
                f.write ("\n")
                f.write ("basis=avdz\n")
#                f.write ("dkroll=1\n")
#                f.write ("dkho=2\n")
                f.write ("{hf;wf,charge=1,spin=1;accu,20;}\n")
                f.write ("{uccsd(t),maxit=250;wf,charge=1,spin=1;}\n")
                f.write ("\n")
                f.write ("---\n")
                f.close
                print count

#This surely does not work correctly yet. I'll get it done later
#Generate energy.dat Crop Script
f=open('inp/crop', 'w')
f.write("mol='mgnn'\n")
f.write("cc=1\n")
f.write("\nfile = open('energy.dat')\n")
f.write("f=open('%s_energies.dat' %mol, 'w')\n")
f.write("for line in file:\n")
f.write("       nrg= line.strip().split()\n")
f.write("       print cc,nrg[6]\n")
f.write("       cc+=1\n")
f.write("       f.write('%s\\n' %nrg[6])\n")
f.write("\nf.close")
f.close

#Append energy.dat creation and cropping
#f=open('inp/submit', 'a')
#f.write ('grep "CCSD(T) total energy" */output.dat > energy.dat\n')
#f.write ("python crop")
#f.close
#
##Make submit script executable
#os.chmod("inp/submit", 0755)
