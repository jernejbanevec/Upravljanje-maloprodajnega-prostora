#strategija skupnega prostora

def SC(i, tau1, j, theta1, c, s):
    if i == j:
        resitev = c[i] * s[i] * (1 + theta1[i])
    elif i > j:
        resitev = c[i] * s[i] * (tau1[i] - tau1[j] + theta1[i])
    else:
        resitev = c[i] * s[i] * (tau1[i] - tau1[j] + 1 + theta1[i])
    return resitev


def vrni_tau(s, s_vrednosti):
    # Funkcija, ki zlozi narobe sestavljen tau (tau0 tau1 tau10 tau2 ...) v prav vrstni red
    n1 = len(s)
    if n1 <= 10:
        return s_vrednosti[0: (n1)]
    else:
        return s_vrednosti[0:3] + s_vrednosti[(n1 - 10 + 2):(n1)] + s_vrednosti[3:(n1 - 10 + 2)]


def naredi_tau(M):
    tau = []
    for i in range(M):
        tau.append(i/M)
    return tau


def iz_tau_t(tau, T):
    # Funkcija, ki zlozi matriko t iz vektorja tau
    n = len(tau)
    t = [[0 for x in range(n)] for y in range(n)]
    for i in range(n):
        for j in range(i):
            t[i][j] = T + tau[j] - tau[i]
        for j in range(i+1, n):
            t[i][j] = tau[j] - tau[i]
    return t


def resi_CAPP(d, v, t, T, H, k, C, c, w, theta):
    # Funkcija, ki resi CAPP oz g(T, t)
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
    for i in range(n):
        s.append(sum(w[i][j] * d[j] * x[i][j].varValue for j in range(n)))
    return (pulp.value(CAPP.objective), s)

# algoritem strategije skupnega prostora

def strategija_skupnega_prostora(d, v, k, theta, C, c, w, H, koraki_max=100, okolica=0.01):
    koraki = 1  # števec korakov
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
        beta = 0
        for i in range(velikost_t):
            beta_i = s[i] * c[i]
            koef = 0
            for j in range(i+1):
                koef += s[j] * c[j]
            beta_i *= koef
            delitelj += s[i] * c[i]
            beta += beta_i
        beta = beta / delitelj


        # Optimalen T
        T = min(math.sqrt(np.dot(k, y) / np.dot(H, s)), C / beta)

        # iz CRSP poiščemo optimalen t, za dane T, y in s
        opt_tau = naredi_tau(velikost_t)
        t = iz_tau_t(opt_tau, T)

        # iz CAPP poiščemo optimalen s, za dane T, t
        (vrednost_g, s) = resi_CAPP(d, v, t, T, H, k, C, c, w, theta)

        delitelj = 0
        beta = 0
        for i in range(velikost_t):
            beta_i = s[i] * c[i]
            koef = 0
            for j in range(i+1):
                koef += s[j] * c[j]
            beta_i *= koef
            delitelj += s[i] * c[i]
            beta += beta_i
        beta = beta / delitelj

        T = min(math.sqrt(np.dot(k, y) / np.dot(H, s)), C / beta)

        vrednost_f_meja = np.dot(v, s) - T * np.dot(H, s) - (1 / T) * np.dot(k, y)

        if vrednost_f_meja < spodnja_meja + gamma:
            break
        else:
            spodnja_meja = vrednost_f_meja
            koraki += 1

    # poračunam vrednost pri "Capacitated problem with independent replenishments
    vrednost_skupni = sum((v[i] * s[i] - H[i] * s[i] * T - (k[i] * y[i]) / T) for i in range(velikost_t))
    Q = []
    for i in range(len(s)):
        Q.append(s[i]*T)
    return vrednost_skupni, y, T, Q, opt_tau

