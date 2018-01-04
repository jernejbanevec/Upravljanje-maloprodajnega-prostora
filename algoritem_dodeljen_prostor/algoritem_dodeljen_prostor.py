import numpy
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

def opt_T(lam, y, s, th, c, H, k):
    #Funkcija vrne seznam optimalnih časov dopolnjenjevanja zalog T[i] pri danih parametrih.
    return [((x0 * x1) / (x2 * ((1 + x3) * x4 * lam + x5))) ** 0.5 for x0, x1, x2, x3, x4, x5 in zip(k, y, s, th, c, H)]

def pogoj_prostor(lam, y, s, th, c, H, k, C):
    #Funkcija vrne pozitivno število, če je pogoj prostora prekršen in nepozitivno, če je pogoju zadoščeno, pri danih paramterih.
    T = opt_T(lam, y, s, th, c, H, k)
    z = -C
    for i in range(len(y)):
        z += (1 + th[i]) * c[i] * s[i] * T[i]
    return z

def resi_DSS(d, v, k, th, C, c, w, H, T):
    # Reši linearni program DSS(dedication space strategy) - maksimizacija profita pri strategiji danega prostora za dane parametre.
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
    DSS += pulp.lpSum((1+th[i])*c[i]*s[i]*T[i] for i in range(n)) <= C
    DSS.solve()
    s = []
    #for v in DSS.variables():
        #print(v.name, v.varValue)
    for i in range(n):
        s.append(sum(w[i][j]*d[j]*x[i][j].varValue for j in range(n)))
    return (pulp.value(DSS.objective), s)

resi_DSS([132.928, 86.8], [13.293, 8.68], [87.155, 56.0], [8.658, 3.036], 315.59999999999997, [0.134, 0.086], [[1,0.5],[0.5,1]], [1.227172, 0.304096], [1.2918421810493985, 1.5624244657542934])

def dodeljen_prostor(d,v,k,th,C,c,w,eps):
    n = len(d)
    H = [a*(0.5 + b) for a,b in zip(c,th)]
    s = d[:]
    y = []
    for i in s:
        if i > 0:
            y.append(1)
        else:
            y.append(0)
    l = 0
    s1 = [0]*n
    while  numpy.linalg.norm((numpy.array(s)-numpy.array(s1))) > eps and l < 1000:
        lam =  bisekcija_dodeljen_prostor(pogoj_prostor, [0, y, s, th, c, H, k, C], [1000, y, s, th, c, H, k, C])
        l += 1
        T = opt_T(lam, y, s, th, c, H, k)
        s1 = s[:]
        dobicek, s = resi_DSS(d, v, k, th, C, c, w, H, T)
        norma = numpy.linalg.norm((numpy.array(s)-numpy.array(s1)))
    Q = []
    for i in range(n):
        Q.append(s[i]*T[i])
    return (dobicek, Q, s, T)

dodeljen_prostor([132.928, 86.8], [13.293, 8.68], [87.155, 56.0], [8.658, 3.036], 50.59999999999997, [0.134, 0.086], [[1,0.99],[0.99,1]], 0.001)


