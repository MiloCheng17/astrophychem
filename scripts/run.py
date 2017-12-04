#!/usr/bin/env python

from coord_convert import *
from File_info import *
from fopt import *

### internal, cartesian, energies, num_basis
#av5z = fopt('av5z-dk/1.out')
#cvqz = fopt('cvqz-dk/1.out')
#cvqzv = fopt('cvqz-v-dk/1.out')
#keys = av5z.data['variables']
#
#ref_geom = []
#for key in range(len(av5z.data['zmat'])):
#    ref_geom.append(av5z.data['zmat'][key] + (cvqz.data['zmat'][key] - cvqzv.data['zmat'][key]))
#
#inter_cart('dummy','ref.int','ref.xyz',ref_geom,keys)
#gangstrom_bohr('ref.xyz','ref.xyz.bohr')


ref_geom, keys = get_ref_geom('ref.int')
geom_change, energy = get_geom_change('av5z-dk-intder',keys)
new_geom = get_new_geom(ref_geom,geom_change)
#for key in range(len(keys)):
#    print '%-7s %10.6f' % (keys[key],new_geom[key])

inter_cart('dummy','1.inp','1.inp-cart',new_geom,keys)
gangstrom_bohr('1.inp-cart','1.inp-cart.bohr')

