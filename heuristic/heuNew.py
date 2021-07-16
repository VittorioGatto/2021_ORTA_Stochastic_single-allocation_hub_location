# -*- coding: utf-8 -*-
import time
import numpy as np
from utility.ev_obf import ev_obf
from utility.ev_x import ev_x


class HeuNew():
    def __init__(self):
        pass

    def solve(self, dict_data, sam, n_scenarios):

        nodes = dict_data['n_nodes']
        d = dict_data['d']
        f = dict_data['f']
        c = sam.c

        sol_z_old = [0] * nodes
        p = [0] * nodes
        of = 0

        sol_x_old = np.zeros((nodes, nodes, n_scenarios))

        start = time.time()

        for s in range(n_scenarios):

            # summation of all the penalty functions
            tot_pf = 0

            for i in range(nodes):
                # penalty function for each node i
                pf = [0] * nodes
                for j in range(nodes):
                    pf[i] += d[i, j] + d[j, i]
                tot_pf += pf[i]

            cost_row = sum(c[:, :, s], 1)

            for i in range(nodes):
                p[i] = p[i] + ((f[i]) + (sam.O_flow[i, s] + sam.D_flow[i, s]) + (cost_row[i]) + (pf[i]))

        sort_index = np.argsort(p)
        sol_z_old[sort_index[0]] = 1

        for s in range(n_scenarios):
            sol_x_old = ev_x(nodes, d, sol_z_old, sol_x_old, s)

        # Evaluation of Heuristic objective function to compare with GUROBI objective function
        of_old = ev_obf(nodes, f, d, n_scenarios, dict_data['alpha'], sol_z_old, sol_x_old, sam.c, sam.w)

        for w in [2, 3, 4]:

            sol_x = np.zeros((nodes, nodes, n_scenarios))
            sol_z = [0] * nodes

            for i in range(w):
                sol_z[sort_index[i]] = 1

            for s in range(n_scenarios):
                sol_x = ev_x(nodes, d, sol_z, sol_x, s)

            # Evaluation of Heuristic objective function to compare with GUROBI objective function
            of = ev_obf(nodes, f, d, n_scenarios, dict_data['alpha'], sol_z, sol_x, sam.c, sam.w)


            if of < of_old:
                of_old = of
                sol_z_old = sol_z
                sol_x_old = sol_x


        end = time.time()

        comp_time = end - start

        return of_old, sol_z_old, sol_x_old, comp_time
