# -*- coding: utf-8 -*-
import time
import numpy as np
from utility.ev_obf import ev_obf
from utility.ev_x import ev_x


class SimpleHeu():
    def __init__(self):
        pass

    def solve(self, dict_data, sam, n_scenarios):

        # initialization of the variables
        nodes = dict_data['n_nodes']
        d = dict_data['d']
        f = dict_data['f']
        c = sam.c
        sol_z = [0] * nodes
        p = [0] * nodes
        of = 0
        sol_x = np.zeros((nodes, nodes, n_scenarios))

        start = time.time()

        for s in range(n_scenarios):

            # summation of all the distance penalty factors
            tot_pf = 0

            for i in range(nodes):
                # distance penalty factor for each node i
                pf = [0] * nodes
                for j in range(nodes):
                    pf[i] += d[i, j] + d[j, i]
                tot_pf += pf[i]

            # summation of row elements cost for each node
            cost_row = sum(c[:, :, s], 1)

            for i in range(nodes):
                p[i] = p[i] + ((f[i]) + (sam.O_flow[i, s] + sam.D_flow[i, s]) + (cost_row[i]) + (pf[i]))

        # mean of the penalty factors
        avg_prob = np.mean(p)

        # choosing of the hubs with penalty factors below the average
        for i in range(nodes):
            if p[i] < avg_prob:
                sol_z[i] = 1

        for s in range(n_scenarios):
            sol_x = ev_x(nodes, d, sol_z, sol_x, s)

            # Check if there are hubs without links
            ok = False
            for i in range(nodes):
                if sol_z[i] == 1:
                    for j in range(nodes):
                        if sol_x[j, i, s] == 1:
                            # the node is linked, we keep it
                            ok = True
                            break
                if not ok:
                    # not linked to anything, it has to be changed
                    sol_z[i] = 0
                ok = False

            # re-computation of the X matrix
            sol_x = ev_x(nodes, d, sol_z, sol_x, s)

        end = time.time()

        # evaluation of the objective function with given Z and X
        of_v, of = ev_obf(nodes, f, d, n_scenarios, dict_data['alpha'], sol_z, sol_x, sam.c, sam.w)

        comp_time = end - start

        return of, of_v, sol_z, sol_x, comp_time
