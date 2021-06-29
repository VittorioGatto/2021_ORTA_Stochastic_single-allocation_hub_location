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
        #probability vector for each node i
        p = []

        tot = 0
        tot_flow = []

        # for s in range(n_scenarios):
        #     for i in range(nodes):
        #         tot += sam.O_flow[i, s] + sam.D_flow[i, s]
        #     tot_flow.append(tot)
        #
        #     #summation of all the penalty functions
        #     tot_pf = 0
        #
        #     for i in range(nodes):
        #         #penalty function for each node i
        #         pf = [0] * nodes
        #         for j in range(nodes):
        #             pf[i] += d[i, j] + d[j, i]
        #         tot_pf += pf[i]
        #
        #     for i in range(nodes):
        #         p.append(((sam.O_flow[i, s] + sam.D_flow[i, s]) / tot_flow[s]) * (1 - pf[i]/tot_pf))

        for s in range(n_scenarios):
            for i in range(nodes):
                tot += sam.O_flow[i, s] + sam.D_flow[i, s]
            tot_flow.append(tot)

            #summation of all the penalty functions
            tot_pf = 0

            for i in range(nodes):
                #penalty function for each node i
                pf = [0] * nodes
                for j in range(nodes):
                    pf[i] += d[i, j] + d[j, i]
                tot_pf += pf[i]

            cost_row = sum(c[:, :, s], 1)
            cost_row_tot = sum(cost_row)
            for i in range(nodes):
                p.append((1 - f[i] / sum(f)) * ((sam.O_flow[i, s] + sam.D_flow[i, s]) / tot_flow[s]) * (1 - cost_row[i] / cost_row_tot) * (1 - pf[i] / tot_pf))


            avg_prob = np.mean(p)

            tot_cost = sum(c[:, :, s], 1)

            avg_cost = np.mean(tot_cost)

            for i in range(nodes):
                    #thresh = np.random.rand()
                    if tot_cost[i] < avg_cost:
                        if p[i] > avg_prob:
                            sol_z[i] = 1
            p.clear()


        end = time.time()

        comp_time = end - start

        return of, sol_z, sol_x, comp_time
