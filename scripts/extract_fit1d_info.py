import os, sys, re
from numpy import *

outf = sys.argv[1]
with open(outf) as f:
    lines = f.readlines()

for i in range(len(lines)):
    if 'Bond length (Angstroms)' in lines[i]:
        r0 = float(lines[i].split()[-1])
        be = float(lines[i+2].split()[-1])
        wx = float(lines[i+4].split()[-1])
        de = float(lines[i+6].split()[-1])
        w0 = float(lines[i+8].split()[-1])
        al = float(lines[i+10].split()[-1])
        break

#print "%20.5f %20.1f %20.5f %20.2f %20.2f %20.2f" %(r0, be, wx,de, w0, al)
#print "%20.5f %20.1f %20.5f %20.2f %20.2f %20.2f" %(r0, be*33.3564/1000000, wx,de*33.3564/1000000000, w0, al)
print("%20.5f %20.6f %20.2f %20.2f %20.6f %20.6f" %(r0, be*33.3564/1000000, w0, al, wx,de*33.3564/1000000000))
