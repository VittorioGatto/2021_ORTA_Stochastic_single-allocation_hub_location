# -*- coding: utf-8 -*-
import time
import math
import logging

class SimpleHeu():
    def __init__(self):
        pass

    def solve(
        self, dict_data, reward, n_scenarios,
    ):
        sol_x = [0] * dict_data['n_items']
        of = -1
        
        start = time.time()
        ratio = [0] * dict_data['n_items']
        for i in range(dict_data['n_items']):
            ratio[i] = dict_data['profits'][i] / dict_data['sizes'][i]
        sorted_pos = [ratio.index(x) for x in sorted(ratio)]
        sorted_pos.reverse()
        cap_tmp = 0
        for i, item in enumerate(sorted_pos):
            cap_tmp += dict_data['sizes'][item]
            if cap_tmp > dict_data['max_size']:
                break
            sol_x[item] = 1
        end = time.time()

        comp_time = end - start
        
        return of, sol_x, comp_time
