#!/usr/bin/env python

from coord_convert import *
from File_info import *
from fopt import *

### internal, cartesian, energies, num_basis
av5z  = fopt('data/cucn_av5z-dk-1.out')
cvqz  = fopt('data/cucn_cvqz-dk-1.out')
cvqzv = fopt('data/cucn_cvqz-v-dk-1.out')
av5z.write('data/av5z.info')
cvqz.write('data/cvqz.info')
cvqzv.write('data/cvqzv.info')

keys = av5z.data['variables']

ref_geom = []
for key in range(len(av5z.data['zmat'])):
    ref_geom.append( av5z.data['zmat'][key] + (cvqz.data['zmat'][key] - cvqzv.data['zmat'][key]) )

for key in range(len(keys)):
    print keys[key], ref_geom[key]

inter_cart('dummy','ref.int','ref.xyz',ref_geom,keys)
gangstrom_bohr('ref.xyz','ref.xyz.bohr')
