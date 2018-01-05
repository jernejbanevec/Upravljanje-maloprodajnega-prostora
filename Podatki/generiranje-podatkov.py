# generiranje podatkov

import random as rd
import math

def generiraj_podatke(N = 2 + round(13 * round(rd.uniform(0, 1), 2))):
    #Funkcija generira naključne podatke za N izdelkov, če ne podamo vhodnega podatka, je tudi ta izbira naključna med 2 in 15.
    d = []
    theta = []
    CV = []
    v = []
    k = []
    c = []
    U = round(rd.uniform(0, 1), 2) #naključno število med 0 in 1
    M = N
    C = (5 + 30 * U) * M

    for i in range(0, M): #dopolnimo vse sezname z M naključnimi podatki
        U = round(rd.uniform(0, 1), 2)
        CV_B = 1 + 9 * U
        U = round(rd.uniform(0, 1), 2)
        CV.append(round(U * CV_B,3))

        theta.append(round(1.65 * CV[i],3))
        U = round(rd.uniform(0, 1), 2)
        d2 = 50 + 100 * U
        U = round(rd.uniform(0, 1), 2)
        delta_d = 80 * U
        U = round(rd.uniform(0, 1), 2)
        d.append(round(d2 + (U - 0.5) * delta_d, 3))
        U = round(rd.uniform(0, 1), 2)
        v2 = 5 + 10 * U
        U = round(rd.uniform(0, 1), 2)
        delta_v = 8 * U
        U = round(rd.uniform(0, 1), 2)
        v.append(round(v2 + (U - 0.5)* delta_v,3))

        U = round(rd.uniform(0, 1), 2)
        k2 = 30 + 70 * U
        U = round(rd.uniform(0, 1), 2)
        delta_k = 50 * U
        U = round(rd.uniform(0, 1), 2)
        k.append(round(k2 + (U - 0.5)* delta_k,3))
        U = round(rd.uniform(0, 1), 2)
        c2 = 0.05 + 0.1 * U
        U = round(rd.uniform(0, 1), 2)
        delta_c = 0.09 * U
        U = round(rd.uniform(0, 1), 2)
        c.append(round(c2 + (U - 0.5)* delta_c,3))

    w = [[round(rd.uniform(0, (1/M)), 3) for i in range(M)] for j in range(M)] #matrika substitucije (zaokroženo na 3 decimalke, da je predstavljivo)
    for i in range(M):
        w[i][i] = 1
    return list((d,v,k,theta,C,c,w,H))


def mean(numbers):
    #Funkcija, ki vrne povprečje podanih števil (numbers)
    return float(sum(numbers)) / max(len(numbers), 1)

def primerjava_povprecij(N):
    #Funkcija, ki izračuna povprečje obeh strategij za 150 naključno podanih problemov, za 2 do N izdelkov.
    povprecje_ss = []
    povprecje_ds = []
    for j in range(2, N+1):
        ds = []
        ss = []
        for i in range(150):
            x = generiraj_podatke(j)
            ds.append(dodeljen_prostor(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7])[0])
            ss.append(strategija_skupnega_prostora(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7])[0])
        povprecje_ds.append(mean(ds))
        povprecje_ss.append(mean(ss))
    return povprecje_ds, povprecje_ss

def primerjava_porabe_protora(N):
    #Funkcija, ki izračuna povprečje obeh strategij za 150 naključno generiranih problemov in različnimi C-ji za N izdelkov.
    povprecje_ds = []
    povprecje_ss = []
    for i in range(11):
        ds = []
        ss = []
        for j in range(150):
            x = generiraj_podatke(N)
            C = (3 + 20 * 0.1 * i) * N
            ds.append(dodeljen_prostor(x[0], x[1], x[2], x[3], C, x[5], x[6], x[7])[0])
            ss.append(strategija_skupnega_prostora(x[0], x[1], x[2], x[3], C, x[5], x[6], x[7])[0])
        povprecje_ds.append(mean(ds))
        povprecje_ss.append(mean(ss))
    return povprecje_ds, povprecje_ss
