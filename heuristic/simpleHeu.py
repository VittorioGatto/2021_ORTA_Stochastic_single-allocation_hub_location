# -*- coding: utf-8 -*-
import time
import numpy as np

class SimpleHeu():
    def __init__(self):
        pass

    def solve(self, dict_data, sam, n_scenarios):

        nodes = dict_data['n_nodes']
        d = dict_data['d']
        f = dict_data['f']
        c = sam.c
        sol_z = [0] * nodes
        of = -1
        
        start = time.time()


        for s in range(n_scenarios):
            # probability vector for each node i
            p = []

            #summation of all the penalty functions
            tot_pf = 0

            for i in range(nodes):
                #penalty function for each node i
                pf = [0] * nodes
                for j in range(nodes):
                    pf[i] += d[i, j] + d[j, i]
                tot_pf += pf[i]

            cost_row = sum(c[:, :, s], 1)
            # cost_row_tot = sum(cost_row)
            for i in range(nodes):
                p.append((f[i]) + (sam.O_flow[i, s] + sam.D_flow[i, s]) + (cost_row[i]) + (pf[i]))
            avg_prob = np.mean(p)

            for i in range(nodes):
                if p[i] < avg_prob:
                    sol_z[i] = 1
            p.clear()


        end = time.time()

        comp_time = end - start

        return of, sol_z, sol_x, comp_time
