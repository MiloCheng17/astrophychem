from numpy import *

energy1 = genfromtxt('energy1.dat')
count = 0
energy = [energy1[0]]

for i in range(-4,5):
    for j in range(-4,5):
        for k in range(-4,5):
            for l in range(-4,5):
                for m in range(-4,5):
                    for n in range(3):
                        if abs(i)+abs(j)+abs(k)+abs(l)+abs(m)+abs(2*n) <= 4:
                            if abs(i)+abs(j)+abs(k)+abs(l)+abs(m)+abs(2*n) != 0:
                                count += 1
                                if n != 0:
                                    energy.append(energy1[count])
                                    energy.append(energy1[count])
                                else:
                                    energy.append(energy1[count])

savetxt('energy.dat',energy,fmt="%14.12f")                                    

