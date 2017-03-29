#!/usr/bin/env python

from coord_convert import *
from File_info import *
from fopt import *

### internal, cartesian, energies, num_basis
ref_geom, keys = get_ref_geom('ref.int')
geom_change, energy = get_geom_change('data/cucn_anpass.out')
new_geom = get_new_geom(ref_geom,geom_change)

inter_cart('dummy','1.inp','1.inp-cart',new_geom,keys)
gangstrom_bohr('1.inp-cart','1.inp-cart.bohr')
