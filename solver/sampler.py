# -*- coding: utf-8 -*-

import numpy as np


class Sampler:
    def __init__(self, instance, n_scenarios):
        self.instance = instance
        self.n_scenarios = n_scenarios

        # w is the flow from node i to node j
        pi = np.random.uniform(0.5, 1.5, size=(instance.n_nodes, n_scenarios))
        pj = np.random.uniform(0.5, 1.5, size=(instance.n_nodes, n_scenarios))
        self.w = np.zeros(shape=(instance.n_nodes, instance.n_nodes, n_scenarios))
        for s in range(n_scenarios):
            for i in range(instance.n_nodes):
                for j in range(instance.n_nodes):
                    self.w[i, j, s] = instance.w[i, j]*pi[i, s]*pj[j, s]

        # O_flow is out-coming flow of the node defined like the sum of the column of w matrix
        self.O_flow = np.zeros((np.size(self.w, 0), np.size(self.w, 2)))
        for s in range(n_scenarios):
            self.O_flow[:, s] = self.w[:, :, s].sum(axis=1)

        # D_flow is the in-coming flow of the node defined like the sum of the row of w matrix
        self.D_flow = np.zeros((np.size(self.w, 0), np.size(self.w, 2)))
        for s in range(n_scenarios):
            self.D_flow[:, s] = self.w[:, :, s].sum(axis=0)

        # C is the variable cost of link from j to k
        self.c = np.zeros((np.size(self.w, 0), np.size(self.w, 1), np.size(self.w, 2)))
        for s in range(n_scenarios):
            for j in range(instance.n_nodes):
                for k in range(instance.n_nodes):
                    self.c[j][k][s] = instance.d[j, k] * (instance.chi * self.O_flow[j, s]
                                                          + instance.sigma * self.D_flow[j, s])

