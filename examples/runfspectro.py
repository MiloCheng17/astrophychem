#!/usr/bin/env python

from fspectro import *

tic2 = spectro('data/tic2_spectro.out')
#print tic2.data
#
cucn = spectro('data/cucn_spectro.out')
#print cucn.data
cuoh = spectro('data/cuoh_spectro.out')
#print cuoh.data
arcn = spectro('data/36Arspectro.out')
#print 'vib', arcn.data['vib_state'], sorted(arcn.data['vib_state'].keys())
#print 'Be',  arcn.data['Be']
#print 'Bs',  arcn.data['Bs']
#print 'DJ',  arcn.data['DJ']
#print 'HJ',  arcn.data['HJ']
#print 'De',  arcn.data['De']
#print 'He',  arcn.data['He']

#print 'vib', tic2.data['vib_state'], sorted(tic2.data['vib_state'].keys())
#print 'Be',  tic2.data['Be']
#print 'Bs',  tic2.data['Bs']
#print 'DJ',  tic2.data['DJ'], sorted(tic2.data['DJ'].keys())
#print 'HJ',  tic2.data['HJ']
#print 'De',  tic2.data['De']
#print 'He',  tic2.data['He']
#print tic2.data['taup']
#print arcn.data['taup']
arcn.write('ArCN+.testout')
tic2.write('TiC2.testout')
