#strategija dodeljenega prostora
import numpy as np
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
    y = [pulp.LpVariable('y%d' % i, lowBound=0, upBound=1, cat = pulp.LpInteger) for i in range(n)] #definiramo odločevalne spremenljivke y in pomožne spremenljivke x
    x = [[pulp.LpVariable("x%d,%d" % (i, j), lowBound=0) for j in range(n)] for i in range(n)]
    s = []
    for i in range(n):
        s.append(sum(w[i][j]*d[j]*x[i][j] for j in range(n))) #definiramo efektivno povpraševanje
    DSS += pulp.lpSum(v[i]*s[i] - H[i]*v[i]*T[i] - k[i]*y[i]/T[i] for i in range(n)), 'Z' #maksimizacijska funkcija
    for i in range(n): #postavimo omejitve za x
        for j in range(n):
            DSS += x[i][j] <= y[i]
            if i != j:
                DSS += x[i][j] <= 1 - y[j]
    DSS += pulp.lpSum((1+theta[i])*c[i]*s[i]*T[i] for i in range(n)) <= C #pogoj prostora
    DSS.solve()
    s = []
    for i in range(n):
        s.append(sum(w[i][j]*d[j]*x[i][j].varValue for j in range(n))) #iz rešenega linearnega programa naredimo s
    return (pulp.value(DSS.objective), s)


def dodeljen_prostor(d,v,k,theta,C,c,w,H,eps=0.01):
    #Funkcija reši problem strategije dodeljenega prostora
    #(za dane paodatke nam poda največji dobiček, katere izdelke vključiti v ponudbo, čas cikla polnjenja izdelkov in količino izdelkov ob posameznem polnjenju
    n = len(d) #število izdelkov
    s = d[:]
    y = []
    for i in s:
        if i > 0:
            y.append(1)
        else:
            y.append(0)
    l = 0
    s1 = [0]*n
    while np.linalg.norm((np.array(s)-np.array(s1))) > eps and l < 100: #ponavljamo, dokler si zaporedna s-a nista dovolj blizu oz. dokler ni norma razlike manjša od epsilon
        lam =  bisekcija_dodeljen_prostor(pogoj_prostor, [0, y, s, theta, c, H, k, C], [1000, y, s, theta, c, H, k, C]) #poiščemo najmanjšo nenegativno lambdo, da pri danih parametrih ni kršen pogoj prostora iz DSS
        l += 1
        T = opt_T(lam, y, s, theta, c, H, k) #čas cikla z najboljšo lambdo
        s1 = s[:]
        dobicek, s = resi_DSS(d, v, k, theta, C, c, w, H, T) #za dane podatke rešimo DSS in dobimo dobiček in s
    Q = []
    for i in range(n): #izračunamo Q
        Q.append(s[i]*T[i])
    return (dobicek, y, T, Q)

