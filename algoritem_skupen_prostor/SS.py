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
print(M)                    #Da pozneje preverim če je dolžina vektorja prava
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


import numpy as np
import cvxopt 

#pomožna funkcija za transponiranje matrike oz vektorja
def transpose(m):
    return(list(map(list,list(zip(*m)))))

# algoritem strategije deljenega prostora

koraki = 0   # števec korakov
s = d   # začetna vrednost za končno efektivno stopnjo povpraševanja
velikost_t = len(d)
t = [[0 for x in range(0, velikost_t)] for y in range(0, velikost_t)] # ničelna matrika (začetna vrednost za t_{ij})
T = 0   # začetna vrednost za čas celotnega cikla
spodnja_meja = 0
gamma = 0.001   # dovoljena okolica
S = 100  # največje število korakov
y = [1 for  i in range(0, velikost_t) if s[i] > 0]

def SC (i, tau, j):
    if i == j:
        resitev = c[i] * s[i] * (1 + theta[i])
    elif i > j:
        resitev = c[i] * s[i] * (tau[i] - tau[j] + theta[i])
    else:
        resitev = c[i] * s[i] * (tau[i] - tau[j] + 1 + theta[i])
    return resitev

tau = [0 for  i in range(0, velikost_t)]

while koraki < S:
    # reši f(s), povsod so zamaknjeni indeksi za 1 v levo
    delitelj = 0
    for i in range(0, len(d)):
        beta = s[i]* c[i]
        koef = 0
        for j in range(0, i):
            koef += s[j] * c[j]
        beta *= koef
        delitelj += s[i]* c[i]
    beta = beta / delitelj
    

    # Optimalen T
    T = min(math.sqrt(np.dot(k, y) / np.dot(H, s)), C / beta)

    # iz CRSP poiščemo optimalen t, za dane T, y in s
    
    
    

    # iz CAPP poiščemo optimalen s, za dane T, t in s


    # povečam število korakov za 1
    koraki += 1
    
