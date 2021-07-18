# -*- coding: utf-8 -*-
import logging
import numpy as np

#Random generation DATA

class Instance:
    def __init__(self, sim_setting):
        logging.info("starting simulation...")

        # number of nodes
        self.n_nodes = sim_setting['n_nodes']

        self.alpha = sim_setting['alpha']

        self.chi = sim_setting['chi']

        self.sigma = sim_setting['sigma']

        #f is the fixed cost of the hub node
        self.f = [28766.736921, 28376.761527, 29774.238965, 24301.334212, 25853.461856, 20762.874300, 34166.355726, 33859.209322, 24717.891218, 33686.431972]
        # self.f = np.around(np.random.uniform(sim_setting['low_cost_fixed'], sim_setting['high_cost_fixed'],
        #                                     sim_setting['n_nodes']))


        # # d is the matrix of distances between
        # self.d = np.array([ [ 0,  1,  1,  1,  1, 50, 50, 50, 50, 50],
        #                     [ 1,  0,  1,  1,  1, 50, 50, 50, 50, 50],
        #                     [ 1,  1,  0,  1,  1, 50, 50, 50, 50, 50],
        #                     [ 1,  1,  1,  0,  1, 50, 50, 50, 50, 50],
        #                     [ 1,  1,  1,  1,  0, 50,  1,  1,  1,  1],
        #                     [50, 50, 50, 50, 50,  0,  1,  1,  1,  1],
        #                     [50, 50, 50, 50,  1,  1,  0,  1,  1,  1],
        #                     [50, 50, 50, 50,  1,  1,  1,  0,  1,  1],
        #                     [50, 50, 50, 50,  1,  1,  1,  1,  0,  1],
        #                     [50, 50, 50, 50,  1,  1,  1,  1,  1,  0]])


        self.d = np.around(np.random.uniform(sim_setting['low_d'], sim_setting['high_d'],
                                             size=(sim_setting['n_nodes'], sim_setting['n_nodes'])))
        self.d = (self.d + self.d.T) / 2
        np.fill_diagonal(self.d, 0)



        logging.info(f"n_nodes: {self.n_nodes}")

    def get_data(self):
        logging.info("getting data from instance...")
        return {
            "n_nodes": self.n_nodes,
            "f": self.f,
            "d": self.d,
            "alpha": self.alpha,
            "chi": self.chi,
            "sigma": self.sigma,
        }
