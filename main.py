#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import logging
import numpy as np
from simulator.instanceSampler import InstanceSampler
from simulator.instance import Instance
from solver.stochasticSaphlp import StochasticSaphlp
from heuristic.simpleHeu import SimpleHeu
from heuristic.heuNew import HeuNew
from heuristic.heuNew2 import HeuNew2
from solver.sampler import Sampler
from utility.plot_results import plot_results

#np.random.seed(5)

if __name__ == '__main__':
    log_name = "./logs/main.log"
    logging.basicConfig(
        filename=log_name,
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO, datefmt="%H:%M:%S",
        filemode='w'
    )
    # to select the number of nodes change the xx in ./etc/xx below
    filename = "./etc/10T"

    inst = InstanceSampler(filename)

    # fp = open("./etc/sim_setting.json", 'r')
    # sim_setting = json.load(fp)
    # fp.close()
    # inst = Instance(sim_setting)

    dict_data = inst.get_data()

    # Reward generation
    n_scenarios = 5
    sam = Sampler(inst, n_scenarios)

    prb = StochasticSaphlp()
    of_exact, sol_Z, sol_X, comp_time_exact = prb.solve(dict_data, sam, n_scenarios, verbose=False)
    plot_results(inst, sam, sol_Z, sol_X, n_scenarios)
    print("------ Solution with GUROBI ------")
    print("Obj funct solution:  ", round(of_exact, 2))
    print("Z: ", sol_Z)
    print("Computational time", round(comp_time_exact, 2), "s")
    print("\n")
    print("\n")

    # heuristic solution one

    heu = SimpleHeu()
    of_heu, of_hev_v, sol_heu_z, sol_heu_x, comp_time_heu = heu.solve(dict_data, sam, n_scenarios)

    print("------ Heuristic solution one ------")
    print("Obj funct solution:  ", round(of_heu, 2))
    print("Z: ", sol_heu_z)
    print("Computational time: ", round(comp_time_heu, 2), "s")

    print("------ Comparison ------")
    print("The heuristic is less efficient than GUROBI solution of: ", round((1 - (of_exact/of_heu))*100, 2), "%")
    plot_results(inst, sam, sol_heu_z, sol_heu_x, n_scenarios)
    print("\n")
    print("\n")

    # heuristic solution two

    heu1 = HeuNew()
    of_heu, of_hev_v, sol_heu_z, sol_heu_x, comp_time_heu = heu1.solve(dict_data, sam, n_scenarios)

    print("------ Heuristic solution second ------")
    print("Obj funct solution:  ", round(of_heu, 2))
    print("Z: ", sol_heu_z)
    print("Computational time: ", round(comp_time_heu, 2), "s")

    print("------ Comparison ------")
    print("The heuristic is less efficient than GUROBI solution of: ", round((1 - (of_exact/of_heu))*100, 2), "%")
    plot_results(inst, sam, sol_heu_z, sol_heu_x, n_scenarios)
    print("\n")
    print("\n")

    # heuristic solution three

    heu2 = HeuNew2()
    of_heu, of_hev_v, sol_heu_z, sol_heu_x, comp_time_heu = heu2.solve(dict_data, sam, n_scenarios)

    print("------ Heuristic solution third ------")
    print("Obj funct solution:  ", round(of_heu, 2))
    print("Z: ", sol_heu_z)
    print("Computational time: ", round(comp_time_heu, 2), "s")

    print("------ Comparison ------")
    print("The heuristic is less efficient than GUROBI solution of: ", round((1 - (of_exact / of_heu)) * 100, 2), "%")
    plot_results(inst, sam, sol_heu_z, sol_heu_x, n_scenarios)


    # # printing results of a file
    # file_output = open("./results/exp_general_table.csv", "w")
    # file_output.write("method, of, sol, time\n")
    # file_output.write("{}, {}, {}, {}\n".format("heu", of_heu, sol_heu, comp_time_heu))
    # file_output.write("{}, {}, {}, {}\n".format("exact", of_heu, sol_heu, comp_time_heu))
    # file_output.close()
