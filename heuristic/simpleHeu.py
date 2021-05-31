# -*- coding: utf-8 -*-
import time
import numpy as np

class SimpleHeu():
    def __init__(self):
        pass

    def solve(self, dict_data, sam, n_scenarios):

        nodes = dict_data['n_nodes']
        d = dict_data['d']
        sol_z = [0] * nodes
        of = -1
        
        start = time.time()
        #probability vector for each node i
        p = []

        tot = 0
        tot_flow = []
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

            for i in range(nodes):
                p.append(((sam.O_flow[i, s] + sam.D_flow[i, s]) / tot_flow[s]) * (1 - pf[i]/tot_pf))
                thresh = np.random.rand()
                if p[i] >= thresh:
                    sol_z[i] = 1

        # sol_x = [0] * dict_data['n_items']
        # of = -1
        #
        # start = time.time()
        # ratio = [0] * dict_data['n_items']
        # for i in range(dict_data['n_items']):
        #     ratio[i] = dict_data['profits'][i] / dict_data['sizes'][i]
        # sorted_pos = [ratio.index(x) for x in sorted(ratio)]
        # sorted_pos.reverse()
        # cap_tmp = 0
        # for i, item in enumerate(sorted_pos):
        #     cap_tmp += dict_data['sizes'][item]
        #     if cap_tmp > dict_data['max_size']:
        #         break
        #     sol_x[item] = 1

        end = time.time()

        comp_time = end - start

        return of, sol_z, comp_time
