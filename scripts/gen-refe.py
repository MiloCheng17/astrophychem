#!/usr/bin/env python
### Default sigfig of energy is 12 based on molpro output ###
### usage: python gen-refe.py, need to have energy-old.dat ###

from numpy import *


olde = genfromtxt('energy-old.dat',usecols=-1)

newe = olde - min(olde)

savetxt('energy.dat',newe,fmt='%.12f')
