#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import logging
import numpy as np
from simulator.instance import Instance
from simulator.tester import Tester
from solver.stochasticSaphlp import StochasticSaphlp
from heuristic.simpleHeu import SimpleHeu
from solver.sampler import Sampler
from utility.plot_results import plot_comparison_hist

np.random.seed(0)

if __name__ == '__main__':
    log_name = "./logs/main.log"
    logging.basicConfig(
        filename=log_name,
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO, datefmt="%H:%M:%S",
        filemode='w'
    )

    fp = open("./etc/sim_setting.json", 'r')
    sim_setting = json.load(fp)
    fp.close()



    inst = Instance(sim_setting)
    dict_data = inst.get_data()
    #print(dict_data)
    
    # Reward generation
    n_scenarios = 5
    sam = Sampler(inst,  n_scenarios)

    prb = StochasticSaphlp()
    of_exact, sol_exact, comp_time_exact = prb.solve(dict_data, sam, n_scenarios, verbose=True)
    print("Solution with GUROBI")
    print(of_exact, sol_exact, comp_time_exact)

    # COMPARISON:
    # test = Tester()
    # n_scenarios = 1000
    # reward_1 = sam.sample_stoch(
    #     inst,
    #     n_scenarios=n_scenarios
    # )
    # ris1 = test.solve_second_stages(
    #     inst,
    #     sol_exact,
    #     n_scenarios,
    #     reward_1
    # )
    # reward_2 = sam.sample_stoch(
    #     inst,
    #     n_scenarios=n_scenarios
    # )
    # ris2 = test.solve_second_stages(
    #     inst,
    #     sol_exact,
    #     n_scenarios,
    #     reward_2
    # )
    # plot_comparison_hist(
    #     [ris1, ris2],
    #     ["run1", "run2"],
    #     ['red', 'blue'],
    #     "profit", "occurencies"
    # )

    #heuristic solution

    heu = SimpleHeu()
    of_heu, sol_heu, comp_time_heu = heu.solve(dict_data, reward, n_scenarios)

    print("Heuristic solution")
    print(of_heu, sol_heu, comp_time_heu)

    # printing results of a file
    file_output = open("./results/exp_general_table.csv", "w")
    file_output.write("method, of, sol, time\n")
    file_output.write("{}, {}, {}, {}\n".format("heu", of_heu, sol_heu, comp_time_heu))
    file_output.write("{}, {}, {}, {}\n".format("exact", of_heu, sol_heu, comp_time_heu))
    file_output.close()

