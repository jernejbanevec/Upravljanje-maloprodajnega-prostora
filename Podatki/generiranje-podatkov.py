# generiranje podatkov

import random as rd
import math 


d = []
H = []
theta = []
CV = []
v = []
k = []
c = []
U = round(rd.uniform(0, 1), 2)
M = 5 + round(10 * U)
print(M)                    #Preverim če je dolžina vektorja prava
C = (5 + 30 * U) * M

for i in range(0, M):
    CV_B = 1 + 9 * U
    CV.append(round(U * CV_B,3))
    
    theta.append(round(1.65 * CV[i],3))
                                    
    d2 = 50 + 100 * U
    delta_d = 80 * U
    d.append(round(d2 + (U - 0.5) * delta_d, 3))
    
    v2 = 5 + 10 * U
    delta_v = 8 * U
    v.append(round(v2 + (U - 0.5)* delta_v,3))
    
    N = math.ceil(M / 5)
    
    k2 = 30 + 70 * U
    delta_k = 50 * U
    k.append(round(k2 + (U - 0.5)* delta_k,3))
    
    c2 = 0.05 + 0.1 * U
    delta_c = 0.09 * U
    c.append(round(c2 + (U - 0.5)* delta_c,3))
    
    H.append(round(c[i] * (0.5 + theta[i]),3))
    
    U = round(rd.uniform(0, 1), 2)
    M = 5 + round(10 * U)




