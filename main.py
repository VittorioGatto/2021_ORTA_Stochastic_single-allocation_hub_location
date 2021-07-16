#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import numpy as np
from simulator.instanceSampler import InstanceSampler
from simulator.tester import Tester
from solver.stochasticSaphlp import StochasticSaphlp
from heuristic.simpleHeu import SimpleHeu
from heuristic.heuNew import HeuNew
from heuristic.heuNew2 import HeuNew2
from solver.sampler import Sampler
from utility.plot_results import plot_results

np.random.seed(5)

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
    #fp = open("./etc/sim_setting.json", 'r')
    #sim_setting = json.load(fp)
    #fp.close()
    #inst = Instance(sim_setting)

    dict_data = inst.get_data()

    # Reward generation
    n_scenarios = 5
    sam = Sampler(inst, n_scenarios)

    prb = StochasticSaphlp()
    of_exact, sol_Z, sol_X, comp_time_exact = prb.solve(dict_data, sam, n_scenarios, verbose=False)
    plot_results(inst, sam, sol_Z, sol_X, n_scenarios)
    print("------ Solution with GUROBI ------")
    print("Obj funct solution:  ", of_exact)
    #print("F: ", inst.f)
    print("Z: ", sol_Z)
    print("Computational time", comp_time_exact)
    print("\n")
    print("\n")
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

    # heuristic solution one

    heu = SimpleHeu()
    of_heu, sol_heu_z, sol_heu_x, comp_time_heu = heu.solve(dict_data, sam, n_scenarios)

    print("------ Heuristic solution one ------")
    print("Obj funct solution:  ", of_heu)
    print("Z: ", sol_heu_z)
    print("Computational time: ", comp_time_heu)

    print("------ Comparison ------")
    print("Difference of objective function: ", of_heu - of_exact)
    print("The heuristic is less efficient than GUROBI solution of: ", (1 - (of_exact/of_heu))*100, "%")
    plot_results(inst, sam, sol_heu_z, sol_heu_x, n_scenarios)
    print("\n")
    print("\n")

    # heuristic solution second

    heu1 = HeuNew()
    of_heu, sol_heu_z, sol_heu_x, comp_time_heu = heu1.solve(dict_data, sam, n_scenarios)

    print("------ Heuristic solution second ------")
    print("Obj funct solution:  ", of_heu)
    print("Z: ", sol_heu_z)
    print("Computational time: ", comp_time_heu)

    print("------ Comparison ------")
    print("Difference of objective function: ", of_heu - of_exact)
    print("The heuristic is less efficient than GUROBI solution of: ", (1 - (of_exact/of_heu))*100, "%")
    plot_results(inst, sam, sol_heu_z, sol_heu_x, n_scenarios)
    print("\n")
    print("\n")

    # heuristic solution third

    heu2 = HeuNew2()
    of_heu, sol_heu_z, sol_heu_x, comp_time_heu = heu2.solve(dict_data, sam, n_scenarios)

    print("------ Heuristic solution third ------")
    print("Obj funct solution:  ", of_heu)
    print("Z: ", sol_heu_z)
    print("Computational time: ", comp_time_heu)

    print("------ Comparison ------")
    print("Difference of objective function: ", of_heu - of_exact)
    print("The heuristic is less efficient than GUROBI solution of: ", (1 - (of_exact / of_heu)) * 100, "%")
    plot_results(inst, sam, sol_heu_z, sol_heu_x, n_scenarios)


    # # printing results of a file
    # file_output = open("./results/exp_general_table.csv", "w")
    # file_output.write("method, of, sol, time\n")
    # file_output.write("{}, {}, {}, {}\n".format("heu", of_heu, sol_heu, comp_time_heu))
    # file_output.write("{}, {}, {}, {}\n".format("exact", of_heu, sol_heu, comp_time_heu))
    # file_output.close()
