from simulator.instanceSampler import InstanceSampler
from heuristic.heuNew2 import HeuNew2
from solver.sampler import Sampler
import numpy as np

filename = "./etc/10T"

inst = InstanceSampler(filename)

dict_data = inst.get_data()

# Reward generation
n_scenarios = 100
sam = Sampler(inst, n_scenarios)

heu2 = HeuNew2()
of_heu, of_hev_v, sol_heu_z, sol_heu_x, comp_time_heu = heu2.solve(dict_data, sam, n_scenarios)

print(of_hev_v)
std = np.std(of_hev_v)

print(std)
