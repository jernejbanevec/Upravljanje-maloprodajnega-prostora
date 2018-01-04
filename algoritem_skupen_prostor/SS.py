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
    U = round(rd.uniform(0, 1), 2)
    d2 = 50 + 100 * U
    delta_d = 80 * U
    d.append(round(d2 + (U - 0.5) * delta_d, 3))
    U = round(rd.uniform(0, 1), 2)
    v2 = 5 + 10 * U
    delta_v = 8 * U
    v.append(round(v2 + (U - 0.5)* delta_v,3))
    
    N = math.ceil(M / 5)

    #spreminjal zaradi negativnega dobička
    U = round(rd.uniform(0, 1), 2)
    k2 = 0.03 + 0.07 * U
    delta_k = 0.05 * U
    k.append(round(k2 + (U - 0.5)* delta_k,3))
    U = round(rd.uniform(0, 1), 2)
    c2 = 0.05 + 0.1 * U
    delta_c = 0.09 * U
    c.append(round(c2 + (U - 0.5)* delta_c,3))
    
    H.append(round(c[i] * (0.5 + theta[i]),3))
    
    U = round(rd.uniform(0, 1), 2)

w = [[round(rd.uniform(0, (1/M)), 3) for i in range(M)] for j in range(M)] #zaokroženo na 3 decimalke, da je predstavljivo
for i in range(M):
    w[i][i] = 1
    

koraki = 0   # števec korakov
s = d[:]   # začetna vrednost za končno efektivno stopnjo povpraševanja
velikost_t = len(s)
t = [[0 for x in range(0, velikost_t)] for y in range(0, velikost_t)] # ničelna matrika (začetna vrednost za t_{ij})
tau = [0 for  i in range(0, velikost_t)]
T = 0
y = [1 for i in range(velikost_t) if s[i] > 0]
        
import numpy as np
import pulp 




def SC(i, tau1, j, theta1):
    if i == j:
        resitev = c[i] * s[i] * (1 + theta1[i])
    elif i > j:
        resitev = c[i] * s[i] * (tau1[i] - tau1[j] + theta1[i])
    else:
        resitev = c[i] * s[i] * (tau1[i] - tau1[j] + 1 + theta1[i])
    return resitev

def vrni_s (s, s_vrednosti):
    n1 = len(s)
    if n1 <= 10:
        return s_vrednosti[0: n1]
    else:
        return s_vrednosti[0:2] + s_vrednosti[(n1 - 10 + 2):(n1)] + s_vrednosti[2:(n1 - 10 + 2)]

def vrni_tau (s, s_vrednosti):
    n1 = len(s)
    if n1 <= 10:
        return s_vrednosti[1: (n1+1)]
    else:
        return s_vrednosti[1:3] + s_vrednosti[(n1 - 10 + 3):(n1 + 1)] + s_vrednosti[3:(n1 - 10 + 3)]

def resi_CRSP (v, s, T, H, k, y, C, beta):
    n = len(v)
    CRSP = pulp.LpProblem('CRSP', pulp.LpMinimize)
    #t = [[pulp.LpVariable("x%d,%d" % (i, j), lowBound=0) for j in range(n)] for i in range(n)]
    tau = [pulp.LpVariable('tau%d' % i, lowBound=0, upBound=1) for i in range(n)]
    CRSP += sum(tau[i] for i in range(n)), 'Z'
    for j in range(n):
        CRSP += sum(SC(i, tau, j, theta) for i in range(n)) <= beta
    for i in range(n):
        for j in range(n):
            if j > i:
                CRSP += tau[j] - tau[i] >= 0
    CRSP += sum(tau[i] for i in range(n)) >= 1
    CRSP.solve()
    asa1 = []
    for v in CRSP.variables():
        #print(v.name, v.varValue)
        asa1.append(v.varValue * T)
    print(pulp.value(CRSP.objective))
    vrednost = pulp.value(CRSP.objective) * T
    return (vrednost, vrni_tau(tau, asa1))

def iz_tau_t (tau, T):
    t = [[0 for x in range(0, velikost_t)] for y in range(0, velikost_t)]
    n = len(tau)
    for i in range(n):
        t[i][i] = 0.
        for j in range(i):
            t[i][j] = tau[j] - tau[i]
        for j in range(i, n):
            t[i][j] = T - (tau[j] - tau[i])
    return t


def resi_CAPP (v, t, T, H, k, y, C, w):
    n = len(v)
    CAPP = pulp.LpProblem('CAPP', pulp.LpMaximize)
    lambda1 = [pulp.LpVariable('lambda1%d' % i, lowBound=0, upBound=1) for i in range(n)]
    x = [[pulp.LpVariable("x%d,%d" % (i, j), lowBound=0) for j in range(n)] for i in range(n)]
    s = [pulp.LpVariable('s%d' % i, lowBound=0) for i in range(n)]
    CAPP += np.dot(v, s) - T * np.dot(H, s) - (1 / T) * np.dot(k, y), 'Z' #- sum(lambda1[i] * (n * C - sum(c[j] * s[j] (t[i][j] + T * theta[j]) for j in range(n))) for i in range(n)) NE DELUJE!
    for i in range(n):
        CAPP += s[i] >= sum(w[i][j]*d[j]*x[i][j] for j in range(n))
        CAPP += s[i] <= sum(w[i][j]*d[j]*x[i][j] for j in range(n))
        for j in range(n):
            CAPP += x[i][j] <= y[i]
            if i != j:
                CAPP += x[i][j] <= 1 - y[j]
            CAPP += y[i] == 0 or y[i] == 1
            CAPP += C - sum(c[j] * s[j] * (t[i][j] + T * theta[j]) for j in range(n)) >= 0
    CAPP.solve()
    asa1 = []
    for v in CAPP.variables():
        #print(v.name, v.varValue)
        asa1.append(v.varValue)
    print(pulp.value(CAPP.objective))
    return (pulp.value(CAPP.objective), vrni_s(s, asa1))



# algoritem strategije skupnega prostora

def strategija_skupnega_prostora (d, koraki_max = 50, okolica = 0.01): 
    koraki = 0   # števec korakov
    s = d   # začetna vrednost za končno efektivno stopnjo povpraševanja
    velikost_t = len(d)
    t = [[0 for x in range(0, velikost_t)] for y in range(0, velikost_t)] # ničelna matrika (začetna vrednost za t_{ij})
    spodnja_meja = 0
    T = 0
    gamma = okolica   # dovoljena okolica
    S = koraki_max  # največje število korakov
    tau = [0 for  i in range(0, velikost_t)]

    while koraki < S:
        y = [1 for  i in range(0, velikost_t) if s[i] > 0 ]
        
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
        (vrednost_f, opt_tau) = resi_CRSP(v, s, T, H, k, y, C, beta)
        t = iz_tau_t(opt_tau, T)
        # iz CAPP poiščemo optimalen s, za dane T, t 
        (vrednost_g, s) = resi_CAPP(v, t, T, H, k, y, C, w)


        if vrednost_g < spodnja_meja + gamma:
            break
        else:
            spodnja_meja = vrednost_g
            koraki += 1

    #poračunam vrednost pri "Capacitated problem with independent replenishments
    vrednost_skupni = sum((v[i] * s[i] - H[i] * s[i] * T - (k[i] * y[i]) / T) for i in range(velikost_t))
    return vrednost_skupni
