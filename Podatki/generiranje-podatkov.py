# generiranje podatkov

import random as rd
import math

def generiraj_podatke(N = 5 + round(10 * round(rd.uniform(0, 1), 2))):
    d = []
    H = []
    theta = []
    CV = []
    v = []
    k = []
    c = []
    U = round(rd.uniform(0, 1), 2)
    M = N #5 + round(10 * U)
    #print(M)                    #Da pozneje preverim če je dolžina vektorja prava
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
    return list((d,v,k,theta,C,c,w,H))



strategija_skupnega_prostora(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7])

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def primerjava_povprecij(N):
    ds = []
    ss = []
    for i in range(15):
        x = generiraj_podatke(N)
        ds.append(dodeljen_prostor(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7])[0])
        ss.append(strategija_skupnega_prostora(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7])[0])
    povprecje_ds = mean(ds)
    povprecje_ss = mean(ss)
    return povprecje_ds, povprecje_ss

def primerjava_porabe_protora(N):
    ds = []
    ss = []
    for i in range(11):
        x = generiraj_podatke(N)
        C = (5 + 30 * 0.1 * i) * N
        ds.append(dodeljen_prostor(x[0], x[1], x[2], x[3], C, x[5], x[6], x[7])[0])
        ss.append(strategija_skupnega_prostora(x[0], x[1], x[2], x[3], C, x[5], x[6], x[7])[0])
    povprecje_ds = mean(ds)
    povprecje_ss = mean(ss)
    return povprecje_ds, povprecje_ss
