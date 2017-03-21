from numpy import *

def cbs23m3l(etz,eqz):
    return 4**3/(4**3-3**3)*eqz - 3**3/(4**3-3**3)*etz 

def cbs45m3l(eqz,e5z):
    return 5**3/(5**3-4**3)*e5z - 4**3/(5**3-4**3)*eqz

def cbs56m3l(e5z,e6z):
    return 6**3/(6**3-5**3)*e6z - 5**3/(6**3-5**3)*e5z

def cbs34m3lt(etz,eqz):
    return 5**3/(5**3-4**3)*eqz - 4**3/(5**3-4**3)*etz

def cbs45m3lt(eqz,e5z):
    return 6**3/(6**3-5**3)*e5z - 5**3/(6**3-5**3)*eqz

def cbs34m4l(etz,eqz):
    return 4**4/(4**4-3**4)*eqz - 3**4/(4**4-3**4)*etz

def cbs45m4half(eqz,e5z):
    return 5.5**4/(5.5**4-4.5**4)*e5z - 4.5**4/(5.5**4-4.5**4)*eqz

def cbs24mix(edz,etz,eqz):
    return (edz*(exp(-2)*exp(-(3**2))-exp(-(2**2))*exp(-3)) - exp(-1)*(etz*exp(-(3**2))-exp(-(2**2))*eqz) + exp(-(1**2))*(etz*exp(-3)-exp(-2)*eqz))/(1*(exp(-2)*exp(-(3**2))-exp(-(2**2))*exp(-3)) - exp(-1)*(1*exp(-(3**2))-exp(-(2**2))*1) + exp(-(1**2))*(1*exp(-3)-exp(-2)*1))

def cbs35mix(etz,eqz,e5z):
    return (etz*(exp(-3)*exp(-(4**2))-exp(-(3**2))*exp(-4)) - exp(-2)*(eqz*exp(-(4**2))-exp(-(3**2))*e5z) + exp(-(2**2))*(eqz*exp(-4)-exp(-3)*e5z))/(1*(exp(-3)*exp(-(4**2))-exp(-(3**2))*exp(-4)) - exp(-2)*(1*exp(-(4**2))-exp(-(3**2))*1) + exp(-(2**2))*(1*exp(-4)-exp(-3)*1))

def fci_dtq(ccsd,ccsdt,ccsdtq):
    return (ccsd) / (1 - ((ccsdt - ccsd) / (ccsd)) / (1 - (ccsdtq - ccsdt) / (ccsdt - ccsd)))

def hf_martin(energy1,energy2,L1,L2):
    return energy2+(energy2-energy1)/(exp(9*(sqrt(L2)-sqrt(L1))-log((L2+1)/(L1+1)))-1)

def fci_dtq_r(ccsd,ccsdt,ccsdtq):
    return ccsd*(1+(ccsdt-ccsd)/ccsd - (ccsdtq-ccsdt)/(ccsdt-ccsd))/(1-(ccsdtq-ccsdt)/(ccsdt-ccsd))

def fci_dtq_q(ccsd,ccsdt,ccsdtq):
    return ccsd+0.5*(ccsdt-ccsd)**2/(ccsdtq-ccsdt)*(1-sqrt(1-4*(ccsdtq-ccsdt)/(ccsdt-ccsd)))

def cbs34m4half(etz,eqz):
    return 4.5**4 / (4.5**4 - 3.5**4) * eqz - 3.5**4 / (4.5**4 - 3.5**4) * etz
