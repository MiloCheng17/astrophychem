#!/usr/bin/env python

from fopt import *

av5z = fopt('av5z-dk/1.out')
zmat      = av5z.data['zmat']
variables = av5z.data['variables']
xyz       = av5z.data['xyz']
energies  = av5z.data['energies']
title     = av5z.data['title']
natom     = av5z.data['natom']
nbasis    = av5z.data['nbasis']
atomlist  = av5z.data['atomlist']

av5z.write('av5z.info')
cvqz = fopt('cvqz-dk/1.out')
cvqz.write('cvqz.info')
cvqzv = fopt('cvqz-v-dk/1.out')
cvqzv.write('cvqzv.info')
