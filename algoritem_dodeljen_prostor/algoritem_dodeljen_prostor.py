import numpy as np
import math
import pulp


def bisekcija_dodeljen_prostor(f, a, b, eps=0.01):
    #Funkcija izračuna ničlo dane funkcije f (prilagojena za funkcijo pogoj_prostor)
    c = a[:]
    c[0] = (a[0]+b[0])/2
    if abs(a[0]-b[0]) < eps:
        return b[0]
    elif f(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7])*f(c[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7]) < 0:
        return bisekcija_dodeljen_prostor(f, a, c, eps)
    else:
        return bisekcija_dodeljen_prostor(f, c, b, eps)

def opt_T(lam, y, s, theta, c, H, k):
    #Funkcija vrne seznam optimalnih časov dopolnjenjevanja zalog T[i] pri danih parametrih.
    T = []
    for i in range(len(s)):
        if s[i] == 0:
            T.append(1)
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
    #for v in DSS.variables():
        #print(v.name, v.varValue)
    for i in range(n):
        s.append(sum(w[i][j]*d[j]*x[i][j].varValue for j in range(n)))
    return (pulp.value(DSS.objective), s)

resi_DSS([132.928, 86.8], [13.293, 8.68], [87.155, 56.0], [8.658, 3.036], 315.59999999999997, [0.134, 0.086], [[1,0.5],[0.5,1]], [1.227172, 0.304096], [1.2918421810493985, 1.5624244657542934])

def dodeljen_prostor(d,v,k,theta,C,c,w,eps=0.01):
    #Funkcija reši problem strategije dodeljenega prostora
    n = len(d)
    H = [a*(0.5 + b) for a,b in zip(c,theta)]
    s = d[:]
    y = []
    for i in s:
        if i > 0:
            y.append(1)
        else:
            y.append(0)
    l = 0
    s1 = [0]*n
    while np.linalg.norm((np.array(s)-np.array(s1))) > eps and l < 1000:
        lam =  bisekcija_dodeljen_prostor(pogoj_prostor, [0, y, s, theta, c, H, k, C], [1000, y, s, theta, c, H, k, C])
        l += 1
        T = opt_T(lam, y, s, theta, c, H, k)
        s1 = s[:]
        dobicek, s = resi_DSS(d, v, k, theta, C, c, w, H, T)
    Q = []
    for i in range(n):
        Q.append(s[i]*T[i])
    return (dobicek, Q, s, T,l, H)

dodeljen_prostor([132.928, 86.8], [13.293, 8.68], [47.155, 56.0], [8.658, 3.036], 50.59999999999997, [0.084, 0.086], [[1,0.99],[0.99,1]], 0.001)
dodeljen_prostor([132.928, 86.8], [13.293, 8.68], [87.155, 56.0], [8.658, 3.036], 50.59999999999997, [0.134, 0.086], [[1,0.99],[0.99,1]], 0.001)


def SC(i, tau1, j, theta1, c, s):
    if i == j:
        resitev = c[i] * s[i] * (1 + theta1[i])
    elif i > j:
        resitev = c[i] * s[i] * (tau1[i] - tau1[j] + theta1[i])
    else:
        resitev = c[i] * s[i] * (tau1[i] - tau1[j] + 1 + theta1[i])
    return resitev


def vrni_s(s, s_vrednosti):
    n1 = len(s)
    if n1 <= 10:
        return s_vrednosti[0: n1]
    else:
        return s_vrednosti[0:2] + s_vrednosti[(n1 - 10 + 2):(n1)] + s_vrednosti[2:(n1 - 10 + 2)]


def vrni_tau(s, s_vrednosti):
    n1 = len(s)
    if n1 <= 10:
        return s_vrednosti[1: (n1 + 1)]
    else:
        return s_vrednosti[1:3] + s_vrednosti[(n1 - 10 + 3):(n1 + 1)] + s_vrednosti[3:(n1 - 10 + 3)]


def resi_CRSP(v, s, c, beta, theta):
    n = len(v)
    CRSP = pulp.LpProblem('CRSP', pulp.LpMinimize)
    # t = [[pulp.LpVariable("x%d,%d" % (i, j), lowBound=0) for j in range(n)] for i in range(n)]
    tau = [pulp.LpVariable('tau%d' % i, lowBound=0, upBound=1) for i in range(n)]
    CRSP += sum(tau[i] for i in range(n)), 'Z'
    for j in range(n):
        CRSP += sum(SC(i, tau, j, theta, c, s) for i in range(n)) <= beta
    for i in range(n):
        for j in range((i + 1), n):
            CRSP += tau[j] - tau[i] >= 0
    CRSP += sum(tau[i] for i in range(n)) >= 1
    CRSP.solve()
    asa1 = []
    for v in CRSP.variables():
        # print(v.name, v.varValue)
        # asa1.append(v.varValue * T)
        asa1.append(v.varValue)
    print(pulp.value(CRSP.objective))
    # vrednost = pulp.value(CRSP.objective) * T
    vrednost = pulp.value(CRSP.objective)
    return (vrednost, vrni_tau(tau, asa1))


def iz_tau_t(tau, T):
    n = len(tau)
    t = [[0 for x in range(0, n)] for y in range(0, n)]
    for i in range(n):
        t[i][i] = 0.
        for j in range(i):
            t[i][j] = tau[j] - tau[i]
        for j in range(i, n):
            t[i][j] = T - (tau[j] - tau[i])
    return t


def resi_CAPP(d, v, t, T, H, k, C, c, w, theta):
    n = len(v)
    CAPP = pulp.LpProblem('CAPP', pulp.LpMaximize)
    y = [pulp.LpVariable('y%d' % i, lowBound=0, upBound=1, cat=pulp.LpInteger) for i in range(n)]
    x = [[pulp.LpVariable("x%d,%d" % (i, j), lowBound=0) for j in range(n)] for i in range(n)]
    s = []
    for i in range(n):
        s.append(sum(w[i][j] * d[j] * x[i][j] for j in range(n)))
    CAPP += np.dot(v, s) - T * np.dot(H, s) - (1 / T) * np.dot(k, y), 'Z'
    for i in range(n):
        for j in range(n):
            CAPP += x[i][j] <= y[i]
            if i != j:
                CAPP += x[i][j] <= 1 - y[j]
        CAPP += C - sum(c[j] * s[j] * (t[i][j] + T * theta[j]) for j in range(n)) >= 0
    CAPP.solve()
    s = []
    # for v in CAPP.variables():
    # print(v.name, v.varValue)
    for i in range(n):
        s.append(sum(w[i][j] * d[j] * x[i][j].varValue for j in range(n)))
    # for v in CAPP.variables():
    # print(v.name, v.varValue)
    print(pulp.value(CAPP.objective))
    return (pulp.value(CAPP.objective), s)


# algoritem strategije skupnega prostora

def strategija_skupnega_prostora(d, v, k, theta, C, c, w, H, koraki_max=50, okolica=0.01):
    koraki = 0  # števec korakov
    s = d  # začetna vrednost za končno efektivno stopnjo povpraševanja
    velikost_t = len(d)
    spodnja_meja = 0
    gamma = okolica  # dovoljena okolica
    S = koraki_max  # največje število korakov

    while koraki < S:

        y = []
        for i in range(velikost_t):
            if s[i] > 0:
                y.append(1)
            else:
                y.append(0)

        # reši f(s), povsod so zamaknjeni indeksi za 1 v levo

        delitelj = 0
        for i in range(0, len(d)):
            beta = s[i] * c[i]
            koef = 0
            for j in range(0, i):
                koef += s[j] * c[j]
            beta *= koef
            delitelj += s[i] * c[i]
        beta = beta / delitelj

        # Optimalen T
        T = min(math.sqrt(np.dot(k, y) / np.dot(H, s)), C / beta)

        # iz CRSP poiščemo optimalen t, za dane T, y in s
        (vrednost_f, opt_tau) = resi_CRSP(v, s, c, beta, theta)
        t = iz_tau_t(opt_tau, T)

        # iz CAPP poiščemo optimalen s, za dane T, t
        (vrednost_g, s) = resi_CAPP(d, v, t, T, H, k, C, c, w, theta)

        vrednost_f_meja = np.dot(v, s) - T * np.dot(H, s) - (1 / T) * np.dot(k, y)

        if vrednost_f_meja < spodnja_meja + gamma:
            break
        else:
            spodnja_meja = vrednost_f_meja
            koraki += 1

    # poračunam vrednost pri "Capacitated problem with independent replenishments
    vrednost_skupni = sum((v[i] * s[i] - H[i] * s[i] * T - (k[i] * y[i]) / T) for i in range(velikost_t))
    return vrednost_skupni


strategija_skupnega_prostora([132.928, 86.8], [13.293, 8.68], [87.155, 56.0], [8.658, 3.036], 50.59999999999997,[0.134, 0.086], [[1, 0.99], [0.99, 1]], [1.227172, 0.304096])

