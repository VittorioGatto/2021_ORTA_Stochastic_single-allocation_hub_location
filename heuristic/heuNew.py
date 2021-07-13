# -*- coding: utf-8 -*-
import time
import numpy as np

class HeuNew():
    def __init__(self):
        pass

    def solve(self, dict_data, sam, n_scenarios):

        nodes = dict_data['n_nodes']
        d = dict_data['d']
        f = dict_data['f']
        c = sam.c
        sol_z = [0] * nodes
        sol_best = [0] * nodes
        of_local = 0
        of_best = 0
        of = [0] * nodes
        sol_x = np.zeros((nodes, nodes, n_scenarios))
        best_old = -1
        w = 0
        best = 0
        OUT = False



        start = time.time()


        while w in range(nodes) and OUT == False:
            of_local = 0
            if sol_best[w] == 0:
                sol_z[w] = 1
            for s in range(n_scenarios):
                # Evaluation of_local X with d
                newD = np.zeros((nodes, nodes))

                for j in range(nodes):
                    for i in range(nodes):
                        newD[i, j] = d[i, j]*sol_z[i]

                for i in range(nodes):
                    if sol_z[i] != 1:
                        arr = np.ma.MaskedArray(newD[:, i], newD[:, i] <= 0)
                        sol_x[i, np.ma.argmin(arr), s] = 1

            # Evaluation of_local Heuristic objective function to compare with GUROBI objective function
            for i in range(nodes):
                of_local += f[i] * sol_z[i]

            # objective function 2nd stage - 1st term
            for s in range(n_scenarios):
                temp = 0
                for i in range(nodes):
                    for k in range(nodes):
                        if i != k:
                            temp += sam.c[i, k, s] * sol_x[i, k, s]
                of_local += temp / n_scenarios

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
                        s_term += dict_data['alpha'] * sam.w[i, j, s] * (A + B + C + D)

                        A = 0
                        B = 0
                        C = 0
                        D = 0

                of_local += s_term / n_scenarios

            of[w] = of_local
            print(of_local)
            print(sol_z, "\n")

            if of_best == 0:
                of_best = of_local
            if of_best > of_local:
                of_best = of_local
            of_sol = []

            if w == nodes - 1 and OUT == False:
                #best = of.index(min(of[0:]))
                for p in range(nodes):
                    if sol_best[p] == 0:
                        of_sol.append(of[p])
                best = of_sol.index(min(of_sol))
                sol_best[best] = 1
                #w = 0
                OUT = True
                break
            else:
                for l in range(nodes):
                    if sol_best[l] == 0:
                        sol_z[l] = 0
                    else:
                        sol_z[l] = 1
            of_local = 0
            w = w + 1


        end = time.time()

        comp_time = end - start

        return of[best], sol_best, sol_x, comp_time
