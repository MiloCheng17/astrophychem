#!/usr/bin/env python

from numpy import *
import os, sys, re
from cbs import *
import argparse  

def compositee(avqz,av5z,wcvqz9,wcvqz5):
    ecbs = cbs45m4half(avqz,av5z)
    ecore = wcvqz5 - wcvqz9
    composite = ecbs + ecore
    return composite

def DKH5corr(wcvqzDKH5,wcvqz5): 
    DKH5 = wcvqzDKH5 - wcvqz5
    return DKH5

def fultcorr(avdzccsdt,avdzccsd_t):
    fullt = avdzccsdt - avdzccsd_t
    return fullt

def core0corr(uwcvqz0,uwcvqz5):
    core0 = uwcvqz0 - uwcvqz5
    return core0

def qcorr(uavdzccsdtq,avdzccsd_t):
    qcorr = uavdzccsdtq - avdzccsd_t 
    return qcorr


if __name__ == '__main__':

    avqz = genfromtxt('avqz-dk.dat',usecols=-1)
    av5z = genfromtxt('av5z-dk.dat',usecols=-1)
    wcvqz9 = genfromtxt('wcvqz-dk9.dat',usecols=-1)
    wcvqz5 = genfromtxt('wcvqz-dk5.dat',usecols=-1)
    if os.path.isfile('composite.dat'):
        composite = genfromtxt('composite.dat',usecols=-1)
    else:
        composite = compositee(avqz,av5z,wcvqz9,wcvqz5)
    

    wcvqzDKH5  = genfromtxt('wcvqz-DKH5.dat',usecols=-1)
    avdzccsd_t = genfromtxt('avdz-dk-ccsd_t.dat',usecols=-1)
    avdzccsdt  = genfromtxt('avdz-dk-ccsdt.dat',usecols=-1)
    uavdzccsdt  = genfromtxt('uavdz-dk-ccsdt.dat',usecols=-1)
    uavdzccsdtq = genfromtxt('uavdz-dk-ccsdt_q.dat',usecols=-1)
    uwcvqz0 = genfromtxt('uwcvqz-dk0.dat',usecols=-1)
    uwcvqz5 = genfromtxt('uwcvqz-dk5.dat',usecols=-1)

    tcorr = fultcorr(avdzccsdt,avdzccsd_t)
    ccorr = core0corr(uwcvqz0,uwcvqz5)
    qcorr = qcorr(uavdzccsdtq,avdzccsd_t)
    dcorr = DKH5corr(wcvqzDKH5,wcvqz5)

    savetxt('composite.dat',composite,fmt='%.18f')
    savetxt('composite+DKH5.dat',composite+dcorr,fmt='%.18f')
    savetxt('composite+0core.dat',composite+ccorr,fmt='%.18f')
    savetxt('composite+CCSDT.dat',composite+tcorr,fmt='%.18f')
    savetxt('composite+CCSDTQ.dat',composite+qcorr,fmt='%.18f')
    savetxt('composite+0core+CCSDT.dat',composite+ccorr+tcorr,fmt='%.18f')
    savetxt('composite+DKH5+CCSDT.dat',composite+tcorr+dcorr,fmt='%.18f')
    savetxt('composite+0core+DKH5+CCSDTQ.dat',composite+qcorr+dcorr+ccorr,fmt='%.18f')
