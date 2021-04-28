# -*- coding: utf-8 -*-
import numpy as np


class Sampler:
    def __init__(self):
        pass

    def sample_ev(self, instance, n_scenarios):
        demand = self.sample_stoch(instance, n_scenarios)
        return np.average(demand, axis=1)

    def sample_stoch(self, instance, n_scenarios):
        return np.around(np.absolute(np.random.normal(
            10,
            1,
            size=(instance.n_items, n_scenarios))
        ))
