#strategija dodeljenega prostora
import numpy as np
import math
import pulp


def bisekcija_dodeljen_prostor(f, a, b, eps=0.01):
    #Funkcija izračuna ničlo dane funkcije f (prilagojena za funkcijo pogoj_prostor)
    c = a[:]
    c[0] = (a[0]+b[0])/2
    if abs(a[0]-b[0]) < eps: #če se a in b razlikujeta manj kot epsilon, smo dovolj blizu ničle in jo vrnemo
        return b[0]
    elif f(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7]) * f(c[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7]) < 0:
        return bisekcija_dodeljen_prostor(f, a, c, eps)
    else:
        return bisekcija_dodeljen_prostor(f, c, b, eps)

def opt_T(lam, y, s, theta, c, H, k):
    #Funkcija vrne seznam optimalnih časov dopolnjenjevanja zalog T[i] pri danih parametrih.
    T = []
    for i in range(len(s)):
        if s[i] == 0:
            T.append(1) #lahko pripnemo karkoli pozitivnega, ker se pomnoži kasneje z s ali pa z y
        else:
            T.append(((k[i] * y[i]) / (s[i] * ((1 + theta[i]) * c[i] * lam + H[i]))) ** 0.5)
    return T

def pogoj_prostor(lam, y, s, theta, c, H, k, C):
    #Funkcija vrne pozitivno število, če je pogoj prostora prekršen in nepozitivno, če je pogoju zadoščeno, pri danih paramterih.
    T = opt_T(lam, y, s, theta, c, H, k)
    z = -C
    for i in range(len(y)):
        z += (1 + theta[i]) * c[i] * s[i] * T[i]
    return z

def resi_DSS(d, v, k, theta, C, c, w, H, T):
    #Funkcija reši linearni program DSS(dedication space strategy) - maksimizacija profita pri strategiji danega prostora za dane parametre.
    n = len(v)
    DSS = pulp.LpProblem('DSS', pulp.LpMaximize)
    y = [pulp.LpVariable('y%d' % i, lowBound=0, upBound=1, cat = pulp.LpInteger) for i in range(n)]
    x = [[pulp.LpVariable("x%d,%d" % (i, j), lowBound=0) for j in range(n)] for i in range(n)]
    s = []
    for i in range(n):
        s.append(sum(w[i][j]*d[j]*x[i][j] for j in range(n)))
    DSS += pulp.lpSum(v[i]*s[i] - H[i]*v[i]*T[i] - k[i]*y[i]/T[i] for i in range(n)), 'Z'
    for i in range(n):
        for j in range(n):
            DSS += x[i][j] <= y[i]
            if i != j:
                DSS += x[i][j] <= 1 - y[j]
    DSS += pulp.lpSum((1+theta[i])*c[i]*s[i]*T[i] for i in range(n)) <= C
    DSS.solve()
    s = []
    for i in range(n):
        s.append(sum(w[i][j]*d[j]*x[i][j].varValue for j in range(n)))
    return (pulp.value(DSS.objective), s)

#resi_DSS([132.928, 86.8], [13.293, 8.68], [87.155, 56.0], [8.658, 3.036], 315.59999999999997, [0.134, 0.086], [[1,0.5],[0.5,1]], [1.227172, 0.304096], [1.2918421810493985, 1.5624244657542934])

def dodeljen_prostor(d,v,k,theta,C,c,w,H,eps=0.01):
    #Funkcija reši problem strategije dodeljenega prostora
    n = len(d)
    s = d[:]
    y = []
    for i in s:
        if i > 0:
            y.append(1)
        else:
            y.append(0)
    l = 0
    s1 = [0]*n
    while np.linalg.norm((np.array(s)-np.array(s1))) > eps and l < 100:
        lam =  bisekcija_dodeljen_prostor(pogoj_prostor, [0, y, s, theta, c, H, k, C], [1000, y, s, theta, c, H, k, C])
        l += 1
        T = opt_T(lam, y, s, theta, c, H, k)
        s1 = s[:]
        dobicek, s = resi_DSS(d, v, k, theta, C, c, w, H, T)
    Q = []
    norma = 0
    if l == 100:
        norma = np.linalg.norm((np.array(s) - np.array(s1)))
    for i in range(n):
        Q.append(s[i]*T[i])
    return (dobicek, l, s, T, Q, norma)
#dodeljen_prostor([72.032, 50.0, 170.848], [9.453, 7.0, 9.587], [31, 44, 69], [4.704, 5.046, 11.339], 60.900000000000006, [0.072, 0.084, 0.158], [[1, 0.05, 0.32], [0.269, 1, 0.116], [0.273, 0.148, 1]], [0.375, 0.466, 1.871])

