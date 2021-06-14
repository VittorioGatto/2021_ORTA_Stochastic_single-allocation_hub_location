#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import logging
import numpy as np
#from simulator.instance import Instance
from simulator.instanceSampler import InstanceSampler
from simulator.tester import Tester
from solver.stochasticSaphlp import StochasticSaphlp
from heuristic.simpleHeu import SimpleHeu
from solver.sampler import Sampler
from utility.plot_results import plot_results

np.random.seed(0)

if __name__ == '__main__':
    log_name = "./logs/main.log"
    logging.basicConfig(
        filename=log_name,
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO, datefmt="%H:%M:%S",
        filemode='w'
    )

    filename = "./etc/easy_instance"

    inst = InstanceSampler(filename)
    #fp = open("./etc/sim_setting.json", 'r')
    #sim_setting = json.load(fp)
    #fp.close()
    #inst = Instance(sim_setting)

    dict_data = inst.get_data()

    # Reward generation
    n_scenarios = 1
    sam = Sampler(inst, n_scenarios)

    prb = StochasticSaphlp()
    of_exact, sol_Z, sol_X, comp_time_exact = prb.solve(dict_data, sam, n_scenarios, verbose=False)
    print("Solution with GUROBI")
    print("Obj funct solution:  ", of_exact)
    print("F: \n", inst.f)
    print("Z: \n", sol_Z)
    print("d:", "\n", inst.d)
    for s in range(n_scenarios):
        print("O_flow in scenario:", s, "\n", sam.O_flow[:, s])
        print("D_flow in scenario:", s, "\n", sam.D_flow[:, s])
        print("W flow in scenario:", s, "\n", sam.w[:, :, s])
        print("C in scenario:", s, "\n", sam.c[:, :, s])
        print("X in scenario:", s, "\n", sol_X[:, :, s])
    print("Computational time", comp_time_exact)

    plot_results(inst, sam, sol_Z, sol_X, n_scenarios)

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

    # heuristic solution

    heu = SimpleHeu()
    of_heu, sol_heu, comp_time_heu = heu.solve(dict_data, sam, n_scenarios)

    print("Heuristic solution")
    print(of_heu, sol_heu, comp_time_heu)

    # # printing results of a file
    # file_output = open("./results/exp_general_table.csv", "w")
    # file_output.write("method, of, sol, time\n")
    # file_output.write("{}, {}, {}, {}\n".format("heu", of_heu, sol_heu, comp_time_heu))
    # file_output.write("{}, {}, {}, {}\n".format("exact", of_heu, sol_heu, comp_time_heu))
    # file_output.close()
