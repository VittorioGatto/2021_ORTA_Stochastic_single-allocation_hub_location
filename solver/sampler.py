# -*- coding: utf-8 -*-
import numpy as np


class Sampler:
    def __init__(self, instance, n_scenarios):
        self.instance = instance
        self.n_scenarios = n_scenarios

        #w is the flow from node s to node j
        self.w = np.absolute(np.random.poisson(8, size=(instance.n_nodes, instance.n_nodes, n_scenarios)))
        pii = np.random.uniform(0.5, 1.5, size=(instance.n_nodes, n_scenarios))
        pij = np.random.uniform(0.5, 1.5, size=(instance.n_nodes, n_scenarios))
        for s in range(n_scenarios):
            for i in range(instance.n_nodes):
                for j in range(instance.n_nodes):
                    self.w[j, i, s] = self.w[j, i, s] * pii[i, s]
                    self.w[j, i, s] = self.w[j, i, s] * pij[j, s]


        # self.w = np.array([[[0, 10, 10, 10, 10],
        #                     [10, 0, 10, 10, 10],
        #                     [10, 10, 0, 10, 10],
        #                     [10, 10, 10, 0, 10],
        #                     [10, 10, 10, 10, 0], ],
        #                     [[0, 10, 10, 10, 10],
        #                     [10, 0, 10, 10, 10],
        #                     [10, 10, 0, 10, 10],
        #                     [10, 10, 10, 0, 10],
        #                     [10, 10, 10, 10, 0], ],
        #                     [[0, 10, 10, 10, 10],
        #                     [10, 0, 10, 10, 10],
        #                     [10, 10, 0, 10, 10],
        #                     [10, 10, 10, 0, 10],
        #                     [10, 10, 10, 10, 0], ],
        #                     [[0, 12, 15, 9, 7],
        #                     [12, 0, 10, 10, 6],
        #                     [15, 10, 0, 10, 65],
        #                     [9, 10, 10, 0, 1],
        #                     [7, 6, 65, 1, 0], ],
        #                     [[0, 4, 22, 5, 10],
        #                     [4, 0, 18, 12, 6],
        #                     [22, 18, 0, 10, 5],
        #                     [5, 12, 10, 0, 20],
        #                     [10, 6, 5, 20, 0], ],
        #                     ])

        # O_flow is out-coming flow of the node defined like the sum of the column of w matrix
        self.O_flow = np.zeros((np.size(self.w, 0), np.size(self.w, 2)))
        for s in range(n_scenarios):
            self.O_flow[:, s] = self.w[:, :, s].sum(axis=1)

        # D_flow is the in-coming flow of the node defined like the sum of the row of w matrix
        self.D_flow = np.zeros((np.size(self.w, 0), np.size(self.w, 2)))
        for s in range(n_scenarios):
            self.D_flow[:, s] = self.w[:, :, s].sum(axis=0)

        # C is the variable cost of node from s to j
        self.c = np.zeros((np.size(self.w, 0), np.size(self.w, 1), np.size(self.w, 2)))
        for s in range(n_scenarios):
            for j in range(instance.n_nodes):
                for k in range(instance.n_nodes):

                    self.c[j][k][s] = instance.d[j, k] * (instance.chi * self.O_flow[j, s]
                                                          + instance.sigma * self.D_flow[j, s])
                    # print("cjk:", self.c[j][k][s], "=", "djk:", instance.d[j][k], "*(chi:", instance.chi,
                    #                                                     "* O_flowjs:", self.O_flow[j][s],
                    #                                                     "+ sigma:", instance.sigma,
                    #                                                     "* D_flowjs:", self.D_flow[j][s],")")

