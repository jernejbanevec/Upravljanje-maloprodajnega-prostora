import numpy
import math
import pulp

def bisekcija_dodeljen_prostor(f,a,b,eps=0.01):
    c = a[:]
    c[0] = (a[0]+b[0])/2
    d = a[0]
    if abs(a[0]-b[0]) < eps:
        return a[0]
    elif f(a[0], a[1], a[2],a[3],a[4],a[5],a[6],a[7])*f(c[0], a[1], a[2],a[3],a[4],a[5],a[6],a[7])<0:
        return bisekcija_dodeljen_prostor(f,a,c,eps)
    else:
        return bisekcija_dodeljen_prostor(f,c,b,eps)

def opt_T(lam, y, s, th, c, H, k):
    return [((x0 * x1) / (x2 * ((1 + x3) * x4 * lam + x5))) ** 0.5 for x0, x1, x2, x3, x4, x5 in zip(k, y, s, th, c, H)]

def pogoj_prostor(lam, y, s, th, c, H, k, C):
    T = opt_T(lam, y, s, th, c, H, k)
    z = 0
    for i in range(len(y)):
        z += (1 + th[i]) * c[i] * s[i] * T[i]
    return z - C

def resi_DSS(d,v,k,th,C,c,w,H,T)
    DSS = pulp.LpProblem('DSS', pulp.LpMaximize)
    y = pulp.LpVariable('y', range(len(v)), lowBound=0,upBound=1)
    x = pulp.LpVariable('x', range(len(v)), lowBound=0)
    DSS += pulp.lpSum(v[i]*s[i] for i in range(len(v))) - sum(H[i]*v[i]*T[i] for i in range(len(s))) - sum(k[i]*y[i] for i in range(len(v))), 'Z'
    for i in range(len(s)):
        DSS += s[i] == sum(w[i][j]*d[j]*x[i][j])


def dodeljen_prostor(d,v,k,th,C,c,eps):
    H = [a*(0.5 + b) for a,b in zip(c,th)]
    s = d
    y = []
    for i in s:
        if i > 0:
            y.append(1)
        else:
            y.append(0)
    l = 0
    while l < 1: #numpy.linalg.norm((numpy.array(s)-numpy.array(s1))) < eps & :
        lam =  bisekcija_dodeljen_prostor(pogoj_prostor, [0, y, s, th, c, H, k, C], [10, y, s, th, c, H, k, C])
        l += 1
    return lam

x = [1,2,1]
dodeljen_prostor(x,x,x,x,4,x,0.001)


