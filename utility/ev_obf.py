def ev_obf(nodes, f, d, n_scenarios, alpha, sol_z, sol_x, c, w):
    of_v = [0] * n_scenarios
    of = 0
    of_1 = 0
    # objective function 1st stage
    for i in range(nodes):
        of_1 += f[i] * sol_z[i]

    # objective function 2nd stage - 1st term
    for s in range(n_scenarios):
        temp = 0
        for i in range(nodes):
            for k in range(nodes):
                if i != k:
                    temp += c[i, k, s] * sol_x[i, k, s]
        of_v[s] += temp

    # objective function 2nd stage - 3st term
    A = 0
    B = 0
    C = 0
    D = 0
    for s in range(n_scenarios):
        s_term = 0
        for i in range(nodes):
            for j in range(nodes):
                A = d[i, j] * sol_z[i] * sol_z[j]

                for l in range(nodes):
                    if l != j:
                        B += d[i, l] * sol_z[i] * sol_x[j, l, s]

                for k in range(nodes):
                    if i != k:
                        C += d[k, j] * sol_x[i, k, s] * sol_z[j]

                for l in range(nodes):
                    for k in range(nodes):
                        if i != k:
                            if j != l:
                                D += (d[k, l] * sol_x[i, k, s] * sol_x[j, l, s])
                s_term += alpha * w[i, j, s] * (A + B + C + D)

                A = 0
                B = 0
                C = 0
                D = 0

        of_v[s] += s_term
    of = of_1 + sum(of_v) / n_scenarios
    of_v = of_v + of_1

    return of_v, of
