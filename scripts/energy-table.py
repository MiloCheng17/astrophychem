#!/usr/bin/env python

from numpy import *
import os, sys, re
from cbs import *
from argparse

def compositee(avqz,av5z,wcvqz9,wcvqz5):
    ecbs = cbs45m4half(avqz,av5z)
    ecore = wcvqz5 - wcvqz9
    composite = ecbs + ecore
    return composite

def DKH5corr(qzDKH5,wcvqz5): 
    DKH5 = qzDKH5 - wcvqz5
    return DKH5

def fultcorr(dzccsdt,dzccsdtp):
    fullt = dzccsdt - dzccsdtp
    return fullt

def core0corr(uwcvqz0,uwcvqz5):
    core0 = uwcvqz0 - uwcvqz5
    return core0

def qcorr(avdzQ,avdzT):
    qcorr = avdzQ - avdzT
    return qcorr


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='energy for spectro')
    parser.add_argument('aVQZ-DK',help='aVQZ-DK energy dat')
    parser.add_argument('aV5Z-DK',help='aV5Z-DK energy dat')
    parser.add_argument('wCVQZ-DK9',help='wCVQZ-DK 9core energy dat')
    parser.add_argument('wCVQZ-DK5',help='wCVQZ-DK 5core energy dat')
    parser.add_argument('composite',default=None,help='composite energy dat')
    parser.add_argument('qzDKH5',help='wCVQZ-DK 5core DKH5 energy dat')
    parser.add_argument('dzccsdt',help='aVDZ-DK CCSDT energy dat')
    parser.add_argument('dzccsdtp',help='aVDZ-DK CCSD(T) energy dat')
    parser.add_argument('u5core',help='uncontracted wCVQZ-DK 5core energy dat')
    parser.add_argument('u0core',help='uncontracted wCVQZ-DK 0core energy dat')
    parser.add_argument('avdzQ',help='aVDZ-DK CCSDT(Q) energy dat')
    parser.add_argument('avdzT',help='aVDZ-DK CCSDT energy dat')

    args = parser.parse_args()

    avqz = genfromtxt(args.aVQZ-DK,usecols=-1)
    av5z = genfromtxt(args.aV5Z-DK,usecols=-1)
    wcvqz9 = genfromtxt(args.wCVQZ-DK9,usecols=-1)
    wcvqz5 = genfromtxt(args.wCVQZ-DK5,usecols=-1)
    if args.composite is None:
        composite = compositee(avqz,av5z,wcvqz9,wcvqz5)
    else:
        composite = genfromtxt(args.composite,usecols=-1)
    qzDKH5 = genfromtxt(args.qzDKH5,usecols=-1)
    dzccsdt = genfromtxt(args.dzccsdt,usecols=-1)
    dzccsdtp = genfromtxt(args.dzccsdtp,usecols=-1)
    uwcvqz0 = genfromtxt(args.u0core,usecols=-1)
    uwcvqz5 = genfromtxt(args.u5core,usecols=-1)
    advzQ = genfromtxt(args.avdzQ,usecols=-1)
    advzT = genfromtxt(args.avdzT,usecols=-1)

    tcorr = fultcorr(dzccsdt,dzccsdtp)
    ccorr = core0corr(uwcvqz0,uwcvqz5)
    qcorr = qcorr(avdzQ,avdzT)
    dcorr = DKH5corr(qzDKH5,wcvqz5)

    savetxt('composite.dat',composite)
    savetxt('composite+DKH5.dat',composite+dcorr)
    savetxt('composite+0core.dat',composite+ccorr)
    savetxt('composite+CCSDT.dat',composite+tcorr)
    savetxt('composite+CCSDTQ.dat',composite+qcorr)
    savetxt('composite+0core+CCSDT.dat',composite+ccorr+tcorr)
    savetxt('composite+DKH5+CCSDT.dat',composite+tcorr+dcorr)
    savetxt('composite+0core+DKH5+CCSDTQ.dat',composite+qcorr+dcorr+ccorr)
