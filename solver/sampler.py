# -*- coding: utf-8 -*-
import numpy as np


class Sampler:
    def __init__(self):
        pass

    # def sample_ev(self, instance, n_scenarios):
    #     demand = self.sample_stoch(instance, n_scenarios)
    #     return np.average(demand, axis=1)

    def W_stoch(self, instance, n_scenarios):
        self.W = np.around(np.absolute(np.random.normal(10, 1, size=(instance.n_nodes, instance.n_nodes, n_scenarios))))
        for i in range(n_scenarios):
            self.W[:, :, i] = (self.W[:, :, i] + self.W[:, :, i].T) / 2
            np.fill_diagonal(self.W[:, :, i], 0)
        return self.W

    def O_stoch(self, instance, n_scenarios):
        self.O_flow = []
        for i in range(n_scenarios):
            self.O_flow.append(self.W[:, :, i].sum(axis=1))
        return self.O_flow

    def D_stoch(self, instance, n_scenarios):
        self.D_flow = []
        for i in range(n_scenarios):
            self.D_flow.append(self.W[:, :, i].sum(axis=1))
        return self.D_flow


    def C_stoch(self, instance, n_scenarios):
        self.C = []
        for i in range(n_scenarios):
            scenarios = []
            for j in range(instance.n_nodes):
                row = []
                for k in range(instance.n_nodes):
                    row.append(instance.d[i][k] * (instance.chi * self.O_flow[i] + instance.sigma * self.D_flow[i]))
                scenarios.append(row)
        self.C.append(scenarios)
        return self.C