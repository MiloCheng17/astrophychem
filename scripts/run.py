from coord_convert import *
from File_info import *
from fopt import *
import sys

### need to have a ref.int file here
ref_geom, keys = get_ref_geom('ref.int')
geom_change, energy = get_geom_change('./')

# convert the angle to radius
geom_change[1] = geom_change[1]*180.0/3.14
new_geom = get_new_geom(ref_geom,geom_change)
inter_cart('ref.int','1.inp','1.inp-cart',new_geom,keys)
gangstrom_bohr('1.inp-cart','1.inp-cart.bohr')

get_ff('./fort.9903')
