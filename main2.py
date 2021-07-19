from simulator.instance import Instance
from simulator.instanceSampler import InstanceSampler
from heuristic.heuNew2 import HeuNew2
from solver.sampler import Sampler
import numpy as np
import json

# change the value of mode
# if you want a random dataset set mode to 1
# if you want a fixed dataset set mode to 0
mode = 1

if mode == 0:
    # to select the number of nodes change the xx in ./etc/xx below
    # in order to match a fixed dataset included in the etc folder
    filename = "./etc/40T"
    inst = InstanceSampler(filename)
else:
    # this will generate a random dataset based on the values inside the sim_setting.json file
    fp = open("./etc/sim_setting.json", 'r')
    sim_setting = json.load(fp)
    fp.close()
    inst = Instance(sim_setting)

dict_data = inst.get_data()

# scenario generation
n_scenarios = 100
sam = Sampler(inst, n_scenarios)

heu2 = HeuNew2()
of_heu, of_hev_v, sol_heu_z, sol_heu_x, comp_time_heu = heu2.solve(dict_data, sam, n_scenarios)

# computation of standard deviation, mean, minimum and maximum of the objective function from different scenarios
std_of = np.std(of_hev_v)
mean_of = np.mean(of_hev_v)
min_of = np.min(of_hev_v)
max_of = np.max(of_hev_v)

print("mean: ", mean_of, "\n")
print("std: ", std_of, "\n")
print("min: ", min_of, "\n")
print("max: ", max_of, "\n")
